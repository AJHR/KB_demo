"""Configuracion global del proyecto."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_RAW = ROOT / "data" / "raw"
DATA_VECTOR = ROOT / "data" / "vector"
LANCEDB_PATH = DATA_VECTOR / "lancedb"
MANIFEST_PATH = DATA_VECTOR / "manifest.json"
LOGS = ROOT / "logs"
SOURCES_YAML = ROOT / "config" / "sources.yaml"

USER_AGENT = "SpenceKBDemo/1.0 (research; contacto: demo@spence.local)"

# Rate limiting
MIN_DELAY_SECONDS = 3.0
JITTER_SECONDS = 1.0
THROTTLE_MULTIPLIER_ON_429_503 = 2.0

# Retries
MAX_RETRIES = 3
RETRY_BACKOFF_BASE = 3.0  # 3s, 9s, 27s

# Timeouts
HTTPX_TIMEOUT = 30.0
PLAYWRIGHT_TIMEOUT_MS = 45_000
PLAYWRIGHT_NETWORK_IDLE_MS = 5_000

# Playwright
PW_VIEWPORT = {"width": 1920, "height": 1080}

# Vector store
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_TOKENS = 800
CHUNK_OVERLAP = 150

# Costos marginales: barras objetivo
TARGET_BARS = [
    "Atacama", "Cardones", "Charrua", "Crucero",
    "Pan de Azucar", "Puerto Montt", "Quillota", "Tarapaca",
]

# Logging
SYNC_LOG = LOGS / "sync.log"
SKIPPED_BY_ROBOTS = LOGS / "skipped_by_robots.txt"
AUTH_REQUIRED = LOGS / "auth_required.txt"
FAILED_DOWNLOADS = LOGS / "failed_downloads.txt"

for p in (DATA_RAW, DATA_VECTOR, LANCEDB_PATH, LOGS):
    p.mkdir(parents=True, exist_ok=True)
