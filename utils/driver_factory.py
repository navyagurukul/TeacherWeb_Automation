from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pytest

@pytest.fixture
def driver():
    options = Options()

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ❌ REMOVE this line if present:
    # options.add_argument("--headless=new")

    # ✅ Correct page load strategy
    options.page_load_strategy = "normal"   # OR "eager"

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()