import time
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class StudentReportPage(BasePage):
    # ================= LOCATORS =================

    STUDENT_REPORT_TAB = (By.XPATH, "//span[contains(text(),'Student Report')]")
    REPORT_TOGGLE = (By.XPATH, "//input[@type='checkbox']")

    # Primary dropdown (Class/Grade style label)
    GRADE_DROPDOWN = (
        By.XPATH,
        "//div[@tabindex='0']//div[contains(text(),'Class') or contains(text(),'Grade') or contains(text(),'UKG') or contains(text(),'LKG')]",
    )

    # Assessment view dropdowns ("Select" field style)
    ASSESSMENT_GRADE_DROPDOWN = (
        By.XPATH,
        "(//div[contains(@class,'report')]//div[@tabindex='0'] | //div[normalize-space()='Select']/ancestor::div[@tabindex='0'])[1]",
    )

    GRADE_OPTIONS = (
        By.XPATH,
        "//div[@role='dialog']//div[@tabindex='0' and normalize-space()!='']",
    )

    # ================= ACTIONS =================

    def open_student_report(self):
        self.click(self.STUDENT_REPORT_TAB)

    def _find_clickable_dropdown(self):
        """Return first clickable dropdown from known variants."""
        candidates = [self.GRADE_DROPDOWN, self.ASSESSMENT_GRADE_DROPDOWN]

        for locator in candidates:
            try:
                return self.wait.until(EC.element_to_be_clickable(locator))
            except TimeoutException:
                continue

        # Final fallback in Assessment Result mode: visible "Select" row.
        return self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[normalize-space()='Select']/ancestor::div[@tabindex='0']")
            )
        )

    def open_grade_dropdown(self):
        dropdown = self._find_clickable_dropdown()

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", dropdown
        )
        self.driver.execute_script("arguments[0].click();", dropdown)

    def _select_grade_from_dialog(self, grade_name, retries=2):
        for attempt in range(1, retries + 1):
            try:
                self.open_grade_dropdown()
                self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
                )
                grade = self.wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            f"//div[@role='dialog']//div[normalize-space()='{grade_name}']",
                        )
                    )
                )
                self.driver.execute_script("arguments[0].click();", grade)
                return True
            except (TimeoutException, StaleElementReferenceException):
                if attempt == retries:
                    return False
                time.sleep(0.4)

    def select_all_grades(self):
        print("Selecting all grades...")
        self.wait_for_ui_stable()
        self.open_grade_dropdown()

        grades = self.wait.until(EC.presence_of_all_elements_located(self.GRADE_OPTIONS))
        grade_names = [g.text.strip() for g in grades if g.text.strip()]
        print(f"Grades found: {grade_names}")

        for grade_name in grade_names:
            try:
                self.click(self.GRADE_DROPDOWN)

                grade = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//div[@role='dialog']//div[normalize-space(text())='{grade_name}']"
            ))
        )

                self.driver.execute_script("arguments[0].click();", grade)
                print(f"Selected grade: {grade_name}")
            except Exception as e:
                print(f"Grade failed: {grade_name} -> {e}")

    def get_all_grades(self):
        self.open_grade_dropdown()
        grades = self.wait.until(EC.presence_of_all_elements_located(self.GRADE_OPTIONS))
        return [g.text.strip() for g in grades if g.text.strip()]

    def select_grade(self, grade_name):
        self.click(self.GRADE_DROPDOWN)

        grade = self.wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//div[@role='dialog']//div[normalize-space(text())='{grade_name}']"
            ))
        )
        self.driver.execute_script("arguments[0].click();", grade)
        print(f"Selected grade: {grade_name}")
        time.sleep(1)

    def wait_for_ui_stable(self):
        print("Waiting for UI to stabilize...")
        try:
            self.wait.until(
                EC.invisibility_of_element_located((By.XPATH, "//div[@role='dialog']"))
            )
        except Exception:
            pass

        # Wait until any known dropdown variant exists after view switch.
        self.wait.until(
            lambda d: len(
                d.find_elements(
                    By.XPATH,
                    "//div[@tabindex='0']//div[contains(text(),'Class') or contains(text(),'Grade') or contains(text(),'Select')]",
                )
            )
            > 0
        )
        print("UI stable")

    def enable_Assessment_Result(self):
        print("Switching to Assessment_Result")
        toggle = self.wait.until(EC.element_to_be_clickable(self.REPORT_TOGGLE))

        if not toggle.is_selected():
            self.driver.execute_script("arguments[0].click();", toggle)
            print("Switched to Assessment_Result")
        else:
            print("Already in Assessment_Result")

        time.sleep(1)

    # ================= FULL FLOW =================

    def run_full_student_report_flow(self):
        self.open_student_report()
        self.select_all_grades()
        self.enable_Assessment_Result()
        self.wait_for_ui_stable()
        self.select_all_grades()
        print("Completed full Student Report flow")
