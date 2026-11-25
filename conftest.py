"""Fixtures y hooks globales de pytest.

- driver: abre un navegador NUEVO por cada test (tests independientes).
- hook de reporte: si un test de UI falla, guarda un screenshot con fecha/hora
  y nombre del test, y lo incrusta en el reporte HTML.
"""
import base64
from datetime import datetime

import pytest
from pytest_html import extras
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from utils.config import HEADLESS, SCREENSHOTS_DIR
from utils.logger import get_logger

log = get_logger("conftest")


@pytest.fixture
def driver():
    options = Options()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Evita el popup de "cambiar contraseña" de Chrome en saucedemo
    options.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    log.info("Iniciando Chrome (headless=%s)", HEADLESS)
    drv = webdriver.Chrome(options=options)
    yield drv
    log.info("Cerrando navegador")
    drv.quit()


@pytest.fixture
def logged_in_driver(driver):
    """Driver con sesión iniciada como standard_user."""
    LoginPage(driver).open().login("standard_user", "secret_sauce")
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.extras = getattr(report, "extras", [])

    if report.when == "call":
        log.info("Test %s -> %s (%.2fs)", item.name, report.outcome.upper(), report.duration)

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
        if drv is None:  # test de API: no hay navegador
            return
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in item.name)
        path = SCREENSHOTS_DIR / f"{timestamp}_{safe_name}.png"
        drv.save_screenshot(str(path))
        log.error("Test fallido, screenshot guardado en %s", path)

        b64 = base64.b64encode(path.read_bytes()).decode()
        report.extras.append(extras.png(b64, name=path.name))
