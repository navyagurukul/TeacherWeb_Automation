import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage
import os
from datetime import datetime
import allure
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

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


@pytest.fixture
def logged_in_driver(driver):
    login = LoginPage(driver)
    login.open()
    assert login.login("Sanskruthi School - Nalgonda", "8247282479")

    return driver


def take_screenshot(driver, name="error"):
    driver.save_screenshot(f"{name}.png")
    

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)

        if driver:
            os.makedirs("reports", exist_ok=True)

            file_name = f"reports/{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            driver.save_screenshot(file_name)

            # ✅ Attach to Allure report
            allure.attach.file(
                file_name,
                name="Screenshot on Failure",
                attachment_type=allure.attachment_type.PNG
            )