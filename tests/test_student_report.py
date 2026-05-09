import pytest
from pages.login_page import LoginPage
from pages.student_report_page import StudentReportPage


@pytest.mark.order(4)
@pytest.mark.smoke
@pytest.mark.regression
def test_Student_report(driver):

    login = LoginPage(driver)
    class_report = StudentReportPage(driver)

    login.open()

    assert login.login("Sanskruthi School - Nalgonda", "8247282479")

    print("Login successful")

    class_report.run_full_student_report_flow()
    