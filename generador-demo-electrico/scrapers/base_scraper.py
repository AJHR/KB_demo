"""Base scraper: rate limiting, robots.txt, retries, cache, httpx + playwright."""
from __future__ import annotations

import hashlib
import json
import random
import threading
import time
import urllib.parse
import urllib.robotparser
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import httpx
from loguru import logger
from tenacity import (
    RetryError, retry, retry_if_exception_type,
    stop_after_attempt, wait_exponential,
)

from config import settings as S


class AuthRequiredError(Exception):
    pass


class RobotsDisallowed(Exception):
    pass


class CaptchaDetected(Exception):
    pass


@dataclass
class FetchResult:
    url: str
    status_code: int
    content: bytes
    headers: dict
    from_cache: bool = False
    sha256: str = ""

    def text(self, encoding: str = "utf-8") -> str:
        return self.content.decode(encoding, errors="replace")


@dataclass
class _DomainState:
    last_request_ts: float = 0.0
    current_delay: float = S.MIN_DELAY_SECONDS
    lock: threading.Lock = field(default_factory=threading.Lock)
    robots: Optional[urllib.robotparser.RobotFileParser] = None
    robots_checked: bool = False


_RETRY_STATUSES = {408, 425, 429, 500, 502, 503, 504}


class TransientHTTPError(Exception):
    def __init__(self, status: int, msg: str = ""):
        super().__init__(f"HTTP {status} {msg}")
        self.status = status


class BaseScraper:
    """Cliente compartido. Una sola instancia por proceso."""
    _domains: dict[str, _DomainState] = {}
    _domains_lock = threading.Lock()
    _instance: Optional["BaseScraper"] = None

    def __init__(self):
        self.client = httpx.Client(
            headers={"User-Agent": S.USER_AGENT, "Accept-Language": "es-CL,es;q=0.9,en;q=0.7"},
            timeout=S.HTTPX_TIMEOUT,
            follow_redirects=True,
        )
        self._pw_browser = None
        self._pw_play = None
        BaseScraper._instance = self

    # ---- rate limiting / domain bookkeeping --------------------------------
    def _domain(self, url: str) -> str:
        return urllib.parse.urlparse(url).netloc.lower()

    def _state(self, domain: str) -> _DomainState:
        with self._domains_lock:
            if domain not in self._domains:
                self._domains[domain] = _DomainState()
            return self._domains[domain]

    def _wait_for_slot(self, domain: str):
        st = self._state(domain)
        with st.lock:
            now = time.monotonic()
            elapsed = now - st.last_request_ts
            delay = st.current_delay + random.uniform(-S.JITTER_SECONDS, S.JITTER_SECONDS)
            delay = max(0.0, delay)
            if st.last_request_ts > 0 and elapsed < delay:
                time.sleep(delay - elapsed)
            st.last_request_ts = time.monotonic()

    def _throttle_up(self, domain: str):
        st = self._state(domain)
        st.current_delay = min(st.current_delay * S.THROTTLE_MULTIPLIER_ON_429_503, 120.0)
        logger.warning(f"[{domain}] throttle ↑ delay={st.current_delay:.1f}s")

    # ---- robots.txt --------------------------------------------------------
    def _robots(self, url: str) -> urllib.robotparser.RobotFileParser:
        domain = self._domain(url)
        st = self._state(domain)
        if st.robots_checked:
            return st.robots
        parsed = urllib.parse.urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(robots_url)
        try:
            self._wait_for_slot(domain)
            r = self.client.get(robots_url)
            if r.status_code == 200:
                rp.parse(r.text.splitlines())
                logger.info(f"[{domain}] robots.txt cargado ({len(r.text)} bytes)")
            else:
                logger.warning(f"[{domain}] robots.txt status={r.status_code} (asumiendo permisivo)")
                rp.parse([])
        except Exception as e:
            logger.warning(f"[{domain}] robots.txt error: {e} (asumiendo permisivo)")
            rp.parse([])
        st.robots = rp
        st.robots_checked = True
        return rp

    def can_fetch(self, url: str) -> bool:
        rp = self._robots(url)
        if rp is None:
            return True
        try:
            return rp.can_fetch(S.USER_AGENT, url)
        except Exception:
            return True

    # ---- cache -------------------------------------------------------------
    def _cache_path_for(self, url: str, dest_dir: Path, filename: Optional[str] = None) -> Path:
        if filename is None:
            filename = self._infer_filename(url)
        dest_dir.mkdir(parents=True, exist_ok=True)
        return dest_dir / filename

    def _infer_filename(self, url: str) -> str:
        p = urllib.parse.urlparse(url)
        name = Path(p.path).name or "index.html"
        if "." not in name:
            name = name + ".html"
        return urllib.parse.unquote(name)

    @staticmethod
    def sha256(data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    # ---- core httpx GET ----------------------------------------------------
    @retry(
        reraise=True,
        retry=retry_if_exception_type((TransientHTTPError, httpx.TransportError)),
        stop=stop_after_attempt(S.MAX_RETRIES),
        wait=wait_exponential(multiplier=S.RETRY_BACKOFF_BASE, min=S.RETRY_BACKOFF_BASE, max=60),
    )
    def _raw_get(self, url: str) -> httpx.Response:
        domain = self._domain(url)
        self._wait_for_slot(domain)
        logger.debug(f"GET {url}")
        r = self.client.get(url)
        if r.status_code in (429, 503):
            self._throttle_up(domain)
            raise TransientHTTPError(r.status_code, url)
        if r.status_code in _RETRY_STATUSES:
            raise TransientHTTPError(r.status_code, url)
        return r

    def get(self, url: str, allow_disallowed: bool = False) -> FetchResult:
        if not allow_disallowed and not self.can_fetch(url):
            self._log_skipped_by_robots(url)
            raise RobotsDisallowed(url)
        try:
            r = self._raw_get(url)
        except RetryError as e:
            raise e.last_attempt.exception() from e
        if r.status_code in (401, 403):
            # 403 puede ser auth o WAF; lo registramos como auth_required
            self._log_auth_required(url, r.status_code)
            raise AuthRequiredError(f"{r.status_code} {url}")
        if r.status_code >= 400:
            raise TransientHTTPError(r.status_code, url)
        return FetchResult(
            url=str(r.url), status_code=r.status_code,
            content=r.content, headers=dict(r.headers),
            sha256=self.sha256(r.content),
        )

    # ---- download + cache --------------------------------------------------
    def download(self, url: str, dest_dir: Path, filename: Optional[str] = None,
                 meta: Optional[dict] = None) -> Path:
        """Descarga url -> dest_dir/filename. Si ya existe con mismo hash, no re-descarga."""
        target = self._cache_path_for(url, dest_dir, filename)
        meta_path = target.with_suffix(target.suffix + ".meta.json")
        if target.exists() and meta_path.exists():
            try:
                old = json.loads(meta_path.read_text("utf-8"))
                if "sha256" in old:
                    logger.info(f"CACHE hit {target.name}")
                    return target
            except Exception:
                pass
        try:
            res = self.get(url)
        except (AuthRequiredError, RobotsDisallowed):
            raise
        except Exception as e:
            self._log_failed(url, str(e))
            raise
        target.write_bytes(res.content)
        sidecar = {
            "url": url,
            "fetched_url": res.url,
            "downloaded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "sha256": res.sha256,
            "size_bytes": len(res.content),
            "content_type": res.headers.get("content-type"),
            "extra": meta or {},
        }
        meta_path.write_text(json.dumps(sidecar, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"OK {url} -> {target.relative_to(S.ROOT)} ({len(res.content)} bytes)")
        return target

    # ---- playwright (lazy) -------------------------------------------------
    def _ensure_playwright(self):
        if self._pw_browser is not None:
            return
        from playwright.sync_api import sync_playwright  # lazy import
        self._pw_play = sync_playwright().start()
        self._pw_browser = self._pw_play.chromium.launch(headless=True)

    def playwright_page(self):
        """Returns a Playwright page with our UA and viewport. Use as context manager via close()."""
        self._ensure_playwright()
        context = self._pw_browser.new_context(
            user_agent=S.USER_AGENT,
            viewport=S.PW_VIEWPORT,
            locale="es-CL",
        )
        return context  # caller does context.new_page() and context.close()

    def playwright_get_html(self, url: str, wait_selector: Optional[str] = None) -> str:
        if not self.can_fetch(url):
            self._log_skipped_by_robots(url)
            raise RobotsDisallowed(url)
        domain = self._domain(url)
        self._wait_for_slot(domain)
        ctx = self.playwright_page()
        try:
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=S.PLAYWRIGHT_TIMEOUT_MS)
            if wait_selector:
                page.wait_for_selector(wait_selector, timeout=S.PLAYWRIGHT_TIMEOUT_MS)
            html = page.content()
            if self._looks_like_captcha(html):
                self._log_failed(url, "captcha-detected")
                raise CaptchaDetected(url)
            return html
        finally:
            ctx.close()

    @staticmethod
    def _looks_like_captcha(html: str) -> bool:
        lo = html.lower()
        markers = ("captcha", "verificacion humana", "are you a human", "checking your browser", "cloudflare")
        return any(m in lo for m in markers)

    # ---- logging helpers ---------------------------------------------------
    def _log_skipped_by_robots(self, url: str):
        S.SKIPPED_BY_ROBOTS.parent.mkdir(parents=True, exist_ok=True)
        with S.SKIPPED_BY_ROBOTS.open("a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')}\t{url}\n")
        logger.warning(f"[robots] saltado {url}")

    def _log_auth_required(self, url: str, status: int):
        S.AUTH_REQUIRED.parent.mkdir(parents=True, exist_ok=True)
        with S.AUTH_REQUIRED.open("a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')}\thttp_{status}\t{url}\n")
        logger.warning(f"[auth] {status} {url}")

    def _log_failed(self, url: str, reason: str):
        S.FAILED_DOWNLOADS.parent.mkdir(parents=True, exist_ok=True)
        with S.FAILED_DOWNLOADS.open("a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')}\t{reason}\t{url}\n")
        logger.error(f"[fail] {reason} {url}")

    # ---- teardown ----------------------------------------------------------
    def close(self):
        try:
            self.client.close()
        finally:
            if self._pw_browser is not None:
                try:
                    self._pw_browser.close()
                except Exception:
                    pass
                try:
                    self._pw_play.stop()
                except Exception:
                    pass
                self._pw_browser = None
                self._pw_play = None


def get_shared() -> BaseScraper:
    return BaseScraper._instance or BaseScraper()
