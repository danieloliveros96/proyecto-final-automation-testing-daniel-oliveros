"""Clase base con las acciones comunes que heredan todas las páginas."""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import DEFAULT_TIMEOUT
from utils.logger import get_logger


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)
        self.log = get_logger(self.__class__.__name__)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.log.info("Click en %s", locator)
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        self.log.info("Escribiendo en %s", locator)
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator) -> str:
        return self.find(locator).text
