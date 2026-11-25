from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CART_ITEMS = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def get_item_names(self) -> list[str]:
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
