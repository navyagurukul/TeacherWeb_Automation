from pages.login_page import LoginPage
from pages.student_management_page import StudentManagementPage
import pytest


@pytest.mark.order(6)
@pytest.mark.smoke
@pytest.mark.regression
def test_student_management(driver):
    login = LoginPage(driver)
    sm = StudentManagementPage(driver)

    login.open()
    assert login.login("Sanskruthi School - Nalgonda", "8247282479")

    sm.open_management()   # MUST ADD
    sm.register_student()
    sm.open_student_approval()
    sm.edit_student()
    sm.delete_student()
    
    print("✅ Student Management Test Completed Successfully")
