from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):

    HOME_TAB = (By.XPATH, "//span[text()='Home']")
    LESSON_TAB = (By.XPATH, "//span[text()='Lesson Plan']")
    CLASS_REPORT_TAB = (By.XPATH, "//span[text()='Class Report']")
    STUDENT_REPORT_TAB = (By.XPATH, "//span[text()='Student Report']")
    MANAGEMENT_TAB = (By.XPATH, "//span[text()='Management']")

    def go_to_home(self):
        self.click(self.HOME_TAB)

    def go_to_lesson(self):
        self.click(self.LESSON_TAB)

    def go_to_class_report(self):
        self.click(self.CLASS_REPORT_TAB)

    def go_to_student_report(self):
        self.click(self.STUDENT_REPORT_TAB)

    def go_to_management(self):
        self.click(self.MANAGEMENT_TAB)

    def verify_home_loaded(self):
        return self.is_visible(self.HOME_TAB)