"""Logger común: escribe en reports/test_run.log (y pytest lo muestra en consola)."""
import logging

from utils.config import REPORTS_DIR


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:  # evita handlers duplicados
        return logger

    logger.setLevel(logging.DEBUG)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(REPORTS_DIR / "test_run.log", encoding="utf-8")
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    logger.addHandler(handler)
    return logger
