import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage

BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"


@pytest.mark.ui
def test_add_product_to_cart(logged_in_driver):
    inventory = InventoryPage(logged_in_driver)
    inventory.add_product(BACKPACK)
    inventory.add_product(BIKE_LIGHT)
    assert inventory.get_cart_count() == 2

    inventory.go_to_cart()
    names = CartPage(logged_in_driver).get_item_names()
    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Bike Light" in names


@pytest.mark.ui
def test_remove_product_from_cart(logged_in_driver):
    inventory = InventoryPage(logged_in_driver)
    inventory.add_product(BACKPACK)
    assert inventory.get_cart_count() == 1
    inventory.remove_product(BACKPACK)
    assert inventory.get_cart_count() == 0


@pytest.mark.ui
def test_sort_by_price_low_to_high(logged_in_driver):
    inventory = InventoryPage(logged_in_driver)
    inventory.sort_by("Price (low to high)")
    prices = inventory.get_prices()
    assert prices == sorted(prices)
