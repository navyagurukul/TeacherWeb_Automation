from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class SidebarPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # ✅ FIXED XPATHS (your provided structure)
    DASHBOARD = (By.XPATH, "//*[@id='root']/div/div/div/div[2]/div/div[2]/div/div/div[3]/div/div/div/div")
    PROFILE = (By.XPATH, "//*[@id='root']/div/div/div/div[2]/div/div[2]/div/div/div[4]/div/div/div/div")
    TEST = (By.XPATH, "//*[@id='root']/div/div/div/div[2]/div/div[2]/div/div/div[5]/div/div/div/div")
    UNLOCK_TOPICS = (By.XPATH, "//*[@id='root']/div/div/div/div[2]/div/div[2]/div/div/div[6]/div/div/div/div")
    LOGOUT = (By.XPATH, "//*[@id='root']//div[contains(.,'Logout')]")  # safer fallback

    def click_element(self, locator, name):
        try:
            print(f"➡️ Clicking: {name}")

            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", element
            )

            self.driver.execute_script("arguments[0].click();", element)

            time.sleep(2)

            print(f"✅ Clicked: {name}")

        except Exception as e:
            print(f"❌ Failed to click {name}: {str(e)[:120]}")

    def click_all_sidebar_items(self):
        print("\n🔍 Starting sidebar navigation...\n")

        self.click_element(self.DASHBOARD, "Dashboard")
        self.click_element(self.PROFILE, "Profile")
        self.click_element(self.TEST, "Test")
        self.click_element(self.UNLOCK_TOPICS, "Unlock Topics")
        self.click_element(self.LOGOUT, "Logout")

        print("\n✅ Sidebar navigation completed")