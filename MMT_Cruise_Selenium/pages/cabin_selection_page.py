import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CabinSelectionPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    # --- Locators ---
    # Phase A: Category Selection Page
    _first_category_book_btn = (By.CSS_SELECTOR, 'a[data-ody-id="BookNowButton"]')
    
    # Phase B: Deposit Warning Overlay Popup
    _popup_continue_btn = (By.XPATH, '//div[contains(@class, "modal-footer")]//a[contains(text(), "Continue") or contains(@onclick, "SubmitSelection")]')
    
    # Phase C: Final Stateroom Allocation Page
    _final_stateroom_book_btn = (By.CSS_SELECTOR, 'a[data-ody-id="StateroomBookNowButton"]')

    def book_first_category_deal(self):
        """Scrolls down, selects the primary category card deal and handles the dynamic modal popup."""
        # 1. Scroll down to bring the first category 'Book Now' button into view
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(2)
        
        # 2. Wait for and click the primary category book button using JavaScript safety fallback
        category_btn = self.wait.until(EC.presence_of_element_located(self._first_category_book_btn))
        self.driver.execute_script("arguments[0].click();", category_btn)
        time.sleep(3)

    def handle_deposit_popup_if_present(self):
        """Intercepts and confirms the non-refundable deposit warning modal notification box if it presents itself."""
        try:
            # Short wait since the popup might trigger asynchronously
            popup_wait = WebDriverWait(self.driver, 7)
            continue_btn = popup_wait.until(EC.element_to_be_clickable(self._popup_continue_btn))
            
            # Click the confirmation continue link
            self.driver.execute_script("arguments[0].click();", continue_btn)
            time.sleep(4)
        except Exception:
            # Log structural warning if the page bypassed the warning modal straight to cabin routing
            print("[INFO] Non-refundable dynamic warning overlay modal did not show up or timed out.")

    def select_final_stateroom(self):
        """Scrolls down on the final layout matrix list and confirms the core specific cabin selection ticket."""
        # 1. Scroll slightly down to align layout tracking markers
        self.driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(2)
        
        # 2. Find the final cabin tier confirmation action handler element
        stateroom_btn = self.wait.until(EC.presence_of_element_located(self._final_stateroom_book_btn))
        self.driver.execute_script("arguments[0].click();", stateroom_btn)
        time.sleep(5) # Let the booking form processing environment settle down completely