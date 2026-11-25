import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from utils.data_reader import read_json

CHECKOUT_DATA = read_json("checkout_data.json")
INVALID_CASES = CHECKOUT_DATA["invalid"]


def _go_to_checkout_form(driver):
    inventory = InventoryPage(driver)
    inventory.add_product("sauce-labs-backpack")
    inventory.go_to_cart()
    CartPage(driver).proceed_to_checkout()
    return CheckoutPage(driver)


@pytest.mark.ui
def test_complete_checkout_flow(logged_in_driver):
    """Flujo completo: producto -> carrito -> datos -> finalizar compra."""
    checkout = _go_to_checkout_form(logged_in_driver)
    data = CHECKOUT_DATA["valid"]
    checkout.fill_information(data["first_name"], data["last_name"], data["postal_code"])
    checkout.finish_order()
    assert checkout.get_confirmation_message() == "Thank you for your order!"


@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize("case", INVALID_CASES, ids=[c["message"] for c in INVALID_CASES])
def test_checkout_with_missing_data(logged_in_driver, case):
    checkout = _go_to_checkout_form(logged_in_driver)
    checkout.fill_information(case["first_name"], case["last_name"], case["postal_code"])
    assert case["message"] in checkout.get_error_message()
