import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.cabin_selection_locators import CabinSelectionLocators

class CabinSelectionPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def book_first_category_deal(self):
        """Scrolls down, selects the primary category card deal and handles the dynamic modal popup."""
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(2)
        
        category_btn = self.wait.until(EC.presence_of_element_located(CabinSelectionLocators.FIRST_AVAILABLE_CABIN_BOOK_BUTTON))
        self.driver.execute_script("arguments[0].click();", category_btn)
        time.sleep(3)

    def handle_deposit_popup_if_present(self):
        """Intercepts and confirms the non-refundable deposit warning modal notification box if it presents itself."""
        try:
            popup_wait = WebDriverWait(self.driver, 7)
            continue_btn = popup_wait.until(EC.element_to_be_clickable(CabinSelectionLocators.SELECT_CABIN_BUTTONS))
            self.driver.execute_script("arguments[0].click();", continue_btn)
            time.sleep(4)
        except Exception:
            print("[INFO] Non-refundable dynamic warning overlay modal did not show up or timed out.")

    def select_final_stateroom(self):
        """Scrolls down on the final layout matrix list and confirms the core specific cabin selection ticket."""
        self.driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(2)
        
        stateroom_btn = self.wait.until(EC.presence_of_element_located(CabinSelectionLocators.FINAL_CONFIRM_BOOK_BUTTON))
        self.driver.execute_script("arguments[0].click();", stateroom_btn)
        time.sleep(5)