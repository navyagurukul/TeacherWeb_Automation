import pytest
from pages.login_page import LoginPage

@pytest.mark.order(1)
@pytest.mark.smoke
@pytest.mark.regression
def test_login(driver):
    login = LoginPage(driver)
    login.open()
    assert login.login("Sanskruthi School - Nalgonda", "8247282479")