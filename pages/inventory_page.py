from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEMS = (By.CSS_SELECTOR, ".inventory_item")
    ITEM_PRICES = (By.CSS_SELECTOR, ".inventory_item_price")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    @staticmethod
    def _add_button(product_slug):
        return (By.CSS_SELECTOR, f"[data-test='add-to-cart-{product_slug}']")

    @staticmethod
    def _remove_button(product_slug):
        return (By.CSS_SELECTOR, f"[data-test='remove-{product_slug}']")

    def is_loaded(self) -> bool:
        return self.get_text(self.TITLE) == "Products"

    def add_product(self, product_slug):
        self.log.info("Agregando producto '%s' al carrito", product_slug)
        self.click(self._add_button(product_slug))

    def remove_product(self, product_slug):
        self.log.info("Quitando producto '%s' del carrito", product_slug)
        self.click(self._remove_button(product_slug))

    def get_cart_count(self) -> int:
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def sort_by(self, visible_text):
        self.log.info("Ordenando por '%s'", visible_text)
        Select(self.find(self.SORT)).select_by_visible_text(visible_text)

    def get_prices(self) -> list[float]:
        return [float(p.text.replace("$", "")) for p in self.find_all(self.ITEM_PRICES)]

    def go_to_cart(self):
        self.click(self.CART_LINK)

    def logout(self):
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
