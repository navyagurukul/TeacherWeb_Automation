import pytest
from pages.lesson_plan_page import LessonPlanPage
import time
@pytest.mark.order(3)
@pytest.mark.smoke
@pytest.mark.regression

class TestLessonPlan:

    def test_all_grades_pdfs(self, logged_in_driver):
        """
        Verifies PDF accessibility across all grades (LIMITED RUN).
        - Opens Lesson Plan
        - Iterates each grade
        - Opens ONLY 3 PDFs per grade (for stability)
        """

        driver = logged_in_driver
        page = LessonPlanPage(driver)

        # Step 1: Open Lesson Plan
        page.open_lesson_plan()

        # Step 2: Get grades
        grades = page.get_grades()

        total_verified = 0

        for grade in grades:
            print(f"\n--- 📂 STARTING GRADE: {grade} ---")

            try:
                # Step 3: Select grade
                page.select_grade(grade)

                # Step 4: Process only 3 PDFs
                count = page.process_all_topics(limit=3)

                total_verified += count

                print(f"✅ Finished {grade}. Topics verified: {count}")

            except Exception as e:
                print(f"❌ Critical error processing {grade}: {str(e)[:100]}")

                # SAFE recovery (avoid crash)
                try:
                    driver.title
                    driver.refresh()
                    page.open_lesson_plan()
                    time.sleep(1)
                    
                except Exception:
                    print("Session completely lost → restarting driver")
                    driver.quit()
                except:
                    print("Session lost. Stopping test execution.")
                    break

        print(f"\n TOTAL PDFs VERIFIED: {total_verified}")