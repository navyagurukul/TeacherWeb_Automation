import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def remove_overlay(self):
        try:
            self.driver.execute_script("""
                let overlay = document.querySelector("div[style*='rgba']");
                if (overlay) overlay.remove();
            """)
        except:
            pass

    def scroll_to_element(self, element):
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});", element
        )

    def click(self, locator):
        if isinstance(locator, str):
            locator = (By.XPATH, locator)

        for _ in range(3):
            try:
                element = self.wait.until(EC.presence_of_element_located(locator))
                self.scroll_to_element(element)
                self.wait.until(EC.element_to_be_clickable(locator))
                element.click()
                return
            except:
                try:
                    element = self.driver.find_element(*locator)
                    self.driver.execute_script("arguments[0].click();", element)
                    return
                except:
                    time.sleep(1)

        raise Exception(f"Click failed: {locator}")

    def click_element(self, element):
        try:
            self.scroll_to_element(element)
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, value):
        if isinstance(locator, str):
            locator = (By.XPATH, locator)

        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def find_elements(self, locator):
        if isinstance(locator, str):
            locator = (By.XPATH, locator)

        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def find_element(self, locator):
        if isinstance(locator, str):
            locator = (By.XPATH, locator)

        return self.wait.until(EC.presence_of_element_located(locator))

    def is_visible(self, locator):
        if isinstance(locator, str):
            locator = (By.XPATH, locator)

        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False