from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import os


@pytest.fixture(scope="session")
def driver():

    options = Options()
    # Detect CI environment (GitHub Actions)
    #is_ci = os.getenv("CI") == "true"

    #if is_ci:
        # print("🚀 Running in CI mode (headless)")
        # options.add_argument("--headless=new")
        #options.add_argument("--window-size=1920,1080")
    #else:
        #print("🖥 Running in local mode")
    options.add_argument("--start-maximized")

    # ✅ Stability fixes (keep these)
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # ✅ Prevent renderer issues
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-features=VizDisplayCompositor")

    # ✅ Use WebDriver Manager (important for CI)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://teacher.englishgurukul.in/")

    driver.set_page_load_timeout(90)
    driver.implicitly_wait(10)
    driver.maximize_window()

    yield driver
    #if not is_ci:
        #input("Press ENTER to close browser...")

    print("🛑 Closing browser")
    driver.quit()