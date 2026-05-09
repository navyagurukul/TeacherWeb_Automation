from pages.login_page import LoginPage
from pages.home_page import HomePage
from selenium.webdriver.common.by import By
import pytest
@pytest.mark.order(2)
@pytest.mark.smoke
@pytest.mark.regression

def test_home_page(driver):

    login = LoginPage(driver)
    home = HomePage(driver)

    # Step 1: Open site & login
    login.open()
    assert login.login("Sanskruthi School - Nalgonda", "8247282479"), "Login Failed"

    # Step 2: Navigate to Home
    home.go_to_home()

    # Step 3: Validate Home Page Loaded
    home_text = driver.find_element(By.XPATH, "//span[text()='Home']")
    assert home_text.is_displayed(), "Home page not loaded"

    # Step 4: Validate key sections (based on your UI)
    try:
        dashboard_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'Home')]")
        assert len(dashboard_elements) > 0, "Dashboard content not visible"
    except Exception:
        assert False, "Dashboard validation failed"

    # Step 5: Bottom Navigation validation (important in your UI)
    try:
        bottom_nav = driver.find_elements(By.XPATH, "//span[text()='Lesson Plan'] | //span[text()='Class Report'] | //span[text()='Student Report']")
        assert len(bottom_nav) >= 3, "Bottom navigation missing"
    except Exception:
        assert False, "Bottom navigation validation failed"

    print("Home Page Test Passed")

    driver.quit()