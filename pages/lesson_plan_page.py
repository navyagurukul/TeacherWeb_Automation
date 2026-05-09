import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (StaleElementReferenceException, InvalidSessionIdException, TimeoutException)
class LessonPlanPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ================= LOCATORS =================
    LESSON_PLAN_TAB = (By.XPATH, "//span[normalize-space(text())='Lesson Plan']/parent::a")
    
    # Dropdown Locators
    GRADE_DROPDOWN = (By.XPATH, "//div[@tabindex='0' and .//div[contains(text(),'Grade') or contains(text(),'Class')]]")
    GRADE_OPTIONS = (By.XPATH, "//div[@role='dialog']//div[@tabindex='0'][normalize-space()]")

    #  WHATSAPP-PROOF LOCATOR: Specifically finds pdf.png inside the list, ignoring the header WhatsApp
    PDF_ICONS = (
    By.XPATH,
    "//div[contains(@style,'width: 50px')]//img"
)

    #  FLEXIBLE ACTIVITY LOCATOR: Finds the 'Microschedule' or 'Video' selection
    VIDEO_BTNS = (
    By.XPATH,
    "//button[contains(.,'Video') or contains(.,'Microschedule') or contains(.,'Speaking')]"
)

    # BACK BUTTON: Targets the 'arrowleft.png' your developer shared
    BACK_BTN = (
    By.XPATH,
    "//*[self::button or @role='button'][.//img[contains(@class,'css-9pa8cd')]]"
)
    PDF_CLOSE_BTN = (By.XPATH, "//*[@data-testid='CloseIcon'] | //button[text()='x'] | //button[contains(@class, 'close')]")
    
    PDF_VIEWER = (By.XPATH, "//canvas | //iframe | //embed")

    # ================= ACTIONS =================

    def open_lesson_plan(self):
        tab = self.wait.until(EC.element_to_be_clickable(self.LESSON_PLAN_TAB))
        self.driver.execute_script("arguments[0].click();", tab)
        print("Lesson Plan opened")

    def get_grades(self):
        dropdown = self.wait.until(EC.element_to_be_clickable(self.GRADE_DROPDOWN))
        self.driver.execute_script("arguments[0].click();", dropdown)
        time.sleep(1)

        elems = self.wait.until(EC.presence_of_all_elements_located(self.GRADE_OPTIONS))
        grades = [e.text.strip() for e in elems if e.text.strip()]

        print("Grades found:", grades)
        return grades

    def select_grade(self, grade):
        print(f"\nSelecting grade: {grade}")
        arrow = self.wait.until(EC.element_to_be_clickable(self.GRADE_DROPDOWN))
        self.driver.execute_script("arguments[0].click();", arrow)
        time.sleep(1)
        option = self.wait.until(EC.element_to_be_clickable((
            By.XPATH, f"//div[@role='dialog']//div[normalize-space(text())='{grade}']" )))
        self.driver.execute_script("arguments[0].click();", option)
        time.sleep(0.5)

    def click_pdf_icon(self, index):
        """Stable click for React UI"""
        for _ in range(3):
            try:
                icons = self.wait.until(EC.presence_of_all_elements_located(self.PDF_ICONS))

                if index >= len(icons):
                    return False

                icon = icons[index]

                self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", icon)
                time.sleep(0.5)

                self.driver.execute_script("arguments[0].click();", icon)

                print("PDF icon clicked")

                # wait for activity panel
                self.wait.until(EC.presence_of_element_located(self.VIDEO_BTNS))
                return True

            except StaleElementReferenceException:
                time.sleep(1)

        return False

    def close_pdf(self):
        try:
            self.driver.execute_script("document.body.click();")
            time.sleep(0.5)

            # ESC fallback (VERY IMPORTANT)
            ActionChains(self.driver).send_keys("\ue00c").perform()

            print("PDF closed")

            # HARD WAIT for full cleanup
            time.sleep(1.5)

            # ensure PDF is gone
            WebDriverWait(self.driver, 10).until_not(
                EC.presence_of_element_located(self.PDF_VIEWER)
            )

        except Exception as e:
            print(f"Close PDF issue: {str(e)[:80]}")

    def reset_state(self):
        try:
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

            # wait for DOM to stabilize (not just presence)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.PDF_ICONS)
            )

            time.sleep(1.5)

        except Exception as e:
            print(f"Reset state issue: {str(e)[:80]}")

    def go_back(self):
        try:
            time.sleep(1)

            back_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.BACK_BTN)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", back_btn)
            time.sleep(0.5)

            # re-click fresh element (IMPORTANT)
            self.driver.execute_script("arguments[0].click();", back_btn)

            print("Back clicked")

            time.sleep(1.5)

        except StaleElementReferenceException:
            print("Stale back button → retrying once")

            # RE-FETCH AGAIN (critical fix)
            back_btn = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.BACK_BTN)
            )
            self.driver.execute_script("arguments[0].click();", back_btn)

        except Exception as e:
            print(f"Back failed: {str(e)[:120]}")

    # ================= MAIN FLOW =================

    def process_all_topics(self, limit=3):
        opened = 0
        i = 0
        print("Loading all topics...")

        # STEP 1: SCROLL TO LOAD ALL
        last = 0
        for _ in range(10):
            icons = self.driver.find_elements(*self.PDF_ICONS)

            if len(icons) == last:
                break

            last = len(icons)
            self.driver.execute_script("window.scrollBy(0,1500)")
            time.sleep(1)

        print(f"Found {last} PDF topics")

        # STEP 2: MAIN LOOP
        while i < limit:
            try:
                self.driver.title  # session check

                icons = self.wait.until(
                    EC.presence_of_all_elements_located(self.PDF_ICONS)
                )

                if i >= len(icons):
                    break

                icon = icons[i]
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});", icon
                )
                time.sleep(1)
                

                # CLICK PDF ICON (same as your working script)
                self.driver.execute_script("arguments[0].click();", icon)
                print(f"[{i+1}] Opened")

                # WAIT ACTIVITY SCREEN
                self.wait.until(
                    EC.presence_of_element_located(self.VIDEO_BTNS)
                )

                # CLICK VIDEO / MICROSCHEDULE (same behavior as Excel script)
                try:
                    activity = self.driver.find_element(*self.VIDEO_BTNS)
                    self.driver.execute_script("arguments[0].click();", activity)
                    print("Activity clicked")
                except TimeoutException:
                    print("No activity button found")
                    i += 1
                    continue
                time.sleep(1)
                # WAIT PDF LOAD (same as your working script behavior)
                loaded = False
                for _ in range(2):  # retry once
                    try:
                        WebDriverWait(self.driver, 10).until(
                            lambda d: any(
                                e.is_displayed()
                                for e in d.find_elements(*self.PDF_VIEWER)
                            )
                        )
                        loaded = True
                        break
                    except:
                        time.sleep(1)

                if not loaded:
                    raise TimeoutException("PDF did not load after retry")
                print("PDF loaded successfully")
                time.sleep(2)
                # CLOSE PDF (same logic you confirmed works)
                self.close_pdf()
                # Ensure still in activity screen
                self.wait.until(EC.presence_of_element_located(self.VIDEO_BTNS))
                # Go back
                self.go_back()
                
                self.reset_state()
                # allow React/WebView to settle
                opened += 1
                i += 1
                # move to next only after success
            except TimeoutException:
                print(f"Timeout on PDF {i+1}")
                i += 1
                # skip and continue
            try:
                self.driver.title
                # simple heartbeat check
            except InvalidSessionIdException:
                print("❌ Session lost. Stopping execution.")
                return opened
        print(f"Limited run complete: {opened} PDFs processed")
        return opened