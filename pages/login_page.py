from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import BASE_URL


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.log.info("Abriendo %s", BASE_URL)
        self.driver.get(BASE_URL)
        return self

    def login(self, username, password):
        self.log.info("Login con usuario '%s'", username)
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR)
