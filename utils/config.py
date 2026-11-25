"""Configuración central del framework."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"

BASE_URL = "https://www.saucedemo.com"
API_BASE_URL = "https://jsonplaceholder.typicode.com"

# HEADLESS=true -> el navegador corre sin ventana (útil en CI)
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
DEFAULT_TIMEOUT = 10
