from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import time


class LoginPage(BasePage):

    SEARCH_SCHOOL = (By.XPATH, "//div[contains(text(),'Search your school')]")
    SCHOOL_INPUT = (By.XPATH, "//input[@placeholder='Type here...']")
    PHONE_INPUT = (By.XPATH, "//input[contains(@placeholder,'mobile number')]")
    LOGIN_BTN = (By.XPATH, "//div[text()='Login']")
    HOME_TEXT = (By.XPATH, "//div[text()='Home']")


    def open(self):
        self.driver.get("https://esteacher.englishgurukul.in/")
        time.sleep(3)
        self.wait.until(
            EC.presence_of_element_located(self.SEARCH_SCHOOL)
    )

    def login(self, school, phone):

        self.click(self.SEARCH_SCHOOL)

        self.send_keys(self.SCHOOL_INPUT, school)

        self.wait.until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(text(),'{school}')]"))
    )
        self.click(f"//div[contains(text(),'{school}')]")

        self.send_keys(self.PHONE_INPUT, phone)

        self.click(self.LOGIN_BTN)

    
        time.sleep(5)

    # DEBUG
        current_url = self.driver.current_url
        print("Current URL:", current_url)

    
        if "teacher" in current_url:
            print("Login successful")
            return True

    
        if self.is_visible("//span[contains(text(),'Home')]"):
            print("Login successful (Home visible)")
            return True

        raise Exception("Login failed")