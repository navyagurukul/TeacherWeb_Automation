import pytest
from pages.side_menu_page import SidebarPage
from pages.login_page import LoginPage


@pytest.mark.order(3)
@pytest.mark.smoke
@pytest.mark.regression
class TestSidebarPage:

    def test_sidebar_navigation(self, driver):
        login = LoginPage(driver)
        sidebar = SidebarPage(driver)

        login.open()
        assert login.login("Sanskruthi School - Nalgonda", "8247282479")

        sidebar.click_all_sidebar_items()

        print("✅ Sidebar navigation test completed")