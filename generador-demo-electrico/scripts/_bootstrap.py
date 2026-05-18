"""Anade el root del proyecto al sys.path para que `config` y `scrapers` sean importables."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
