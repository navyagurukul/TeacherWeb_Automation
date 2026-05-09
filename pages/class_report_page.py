import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ClassReportPage(BasePage):

    # ================= LOCATORS =================

    CLASS_REPORT_TAB = (By.XPATH, "//span[contains(text(),'Class Report')]")

    REPORT_TOGGLE = (By.XPATH, "//input[@type='checkbox']")

    GRADE_DROPDOWN = (
        By.XPATH,
        "//div[@tabindex='0']//div[contains(text(),'Class') or contains(text(),'Grade') or contains(text(),'UKG') or contains(text(),'LKG') or contains(text(),'CT') or contains(text(),'ETC')]"
    )

    GRADE_OPTIONS = (By.XPATH, "//div[@role='dialog']//div[@tabindex='0']")

    TOTAL_MONTHLY_TOGGLE = (
        By.XPATH,
        "//div[contains(text(),'Total')]/following::input[1]"
    )

    ASSESSMENT_DROPDOWN = (
    By.XPATH,
    "//div[@tabindex='0'][.//div[contains(text(),'Assessment') or contains(.,'Assesment')]]"
)

    ASSESSMENT_OPTIONS = (
    By.XPATH,
    "//div[@tabindex='0' and (contains(.,'Assessment') or contains(.,'Assesment'))]"
)
    
    
    # ================= ACTIONS =================

    def open_class_report(self):
        self.click(self.CLASS_REPORT_TAB)

    def select_all_grades(self):
        self.wait.until(EC.element_to_be_clickable(self.GRADE_DROPDOWN))
        self.click(self.GRADE_DROPDOWN)

        grades = self.wait.until(
            EC.presence_of_all_elements_located(self.GRADE_OPTIONS)
        )

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
        self.click(self.GRADE_DROPDOWN)
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

    def toggle_total_monthly(self):
        element = self.wait.until(
            EC.element_to_be_clickable(self.TOTAL_MONTHLY_TOGGLE)
        )

        self.driver.execute_script("arguments[0].click();", element)
        print("Total/Monthly toggled")
        time.sleep(1)

    def enable_test_report(self):
        print("Switching to Test Report")

        toggle = self.wait.until(
            EC.element_to_be_clickable(self.REPORT_TOGGLE)
        )

        if not toggle.is_selected():
            self.driver.execute_script("arguments[0].click();", toggle)
            print("Switched to Test Report")
        else:
            print("Already in Test Report")

        time.sleep(2)

    # OPEN DROPDOWN
    def open_assessment_dropdown(self):

        dropdown = self.wait.until(
            EC.element_to_be_clickable(self.ASSESSMENT_DROPDOWN)
    )

        self.driver.execute_script("arguments[0].click();", dropdown)

        print("Assessment dropdown clicked")

        self.wait.until(
            EC.presence_of_element_located(self.ASSESSMENT_OPTIONS)
    )
        
        options = self.driver.find_elements(*self.ASSESSMENT_OPTIONS)
        print(f"DEBUG → options count: {len(options)}")

    def get_assessment_names(self):

        self.open_assessment_dropdown()
        print("Assessment dropdown opened")

        options = self.wait.until(
            EC.presence_of_all_elements_located(self.ASSESSMENT_OPTIONS)
    )
        time.sleep(1)

        assessment_names = []

        for option in options:
            if text:= option.text.strip():
                assessment_names.append(text)

        print(f"Assessments found: {assessment_names}")
        return assessment_names

    def select_all_assessments(self):

        selected_names = set()

        while True:
            try:
            # Step 1: Open dropdown fresh
                self.open_assessment_dropdown()

            # Step 2: Get ALL visible options again
                options = self.wait.until(
                    EC.presence_of_all_elements_located(self.ASSESSMENT_OPTIONS)
            )
                time.sleep(1)

                names = [
                    opt.text.strip() for opt in options if opt.text.strip()
            ]

            # Remove duplicates
                names = list(dict.fromkeys(names))

                print(f"Current visible options: {names}")

            # Step 3: Find next unselected item
                next_to_select = None
                for name in names:
                    if name not in selected_names:
                        next_to_select = name
                        break

                # No new items left → exit loop
                if not next_to_select:
                    print("All assessments selected")
                    return

                print(f"Selecting: {next_to_select}")

            # Step 4: Click it
                option = self.wait.until(
                    EC.element_to_be_clickable((
                        By.XPATH,
                        f"//div[@tabindex='0' and normalize-space()='{next_to_select}']"
                ))
            )

                self.driver.execute_script("arguments[0].click();", option)

                selected_names.add(next_to_select)

                print(f"Selected so far: {selected_names}")

                time.sleep(1)

            except Exception as e:
                print(f"Error: {e}")
                return
        

    def select_assessment_for_each_grade(self):

        grades = self.get_all_grades()

        for grade in grades:
            print(f"\n Processing Grade: {grade}")

            try:
                self.select_grade(grade)

                self.wait.until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
            )

                self.wait.until(
                    EC.element_to_be_clickable(self.ASSESSMENT_DROPDOWN)
            )
                time.sleep(1)
            # select ALL assessments
                self.select_all_assessments()

            except Exception as e:
                print(f"Assessment issue for {grade}: {e}")

    # ================= FULL FLOW =================

    def run_full_class_report_flow(self):
        self.open_class_report()
        self.select_all_grades()
        self.toggle_total_monthly()
        self.enable_test_report()
        self.select_all_grades()
        self.select_assessment_for_each_grade()
        print("Completed full Class Report flow")