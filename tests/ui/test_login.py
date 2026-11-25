import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_reader import read_csv

LOGIN_DATA = read_csv("login_data.csv")


@pytest.mark.ui
@pytest.mark.parametrize(
    "case", LOGIN_DATA, ids=[f"{c['username'] or 'vacio'}-{c['expected']}" for c in LOGIN_DATA]
)
def test_login_data_driven(driver, case):
    """Login con distintos conjuntos de datos leídos desde data/login_data.csv."""
    login = LoginPage(driver).open()
    login.login(case["username"], case["password"])

    if case["expected"] == "success":
        assert InventoryPage(driver).is_loaded(), "No se cargó la página de productos"
    else:
        assert case["message"] in login.get_error_message()


@pytest.mark.ui
def test_logout(logged_in_driver):
    inventory = InventoryPage(logged_in_driver)
    inventory.logout()
    assert "saucedemo.com" in logged_in_driver.current_url
    assert LoginPage(logged_in_driver).find(LoginPage.LOGIN_BUTTON).is_displayed()
