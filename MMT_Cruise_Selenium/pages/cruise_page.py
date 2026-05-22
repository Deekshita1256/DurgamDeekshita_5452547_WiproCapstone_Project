import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CruisePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    # --- Precise Locators from your DevTools Screenshots ---
    _login_modal_close = (By.CSS_SELECTOR, 'span[data-cy="closeModal"]')
    _modal_overlay = (By.CSS_SELECTOR, 'li[data-cy="account"]') 
    _cruise_nav_icon = (By.XPATH, '//a[contains(@href, "/cruise")]|//span[contains(@class, "chCruise")]')
    
    # Input container elements
    _destination_trigger = (By.ID, 'destinationCity')
    _month_trigger = (By.CSS_SELECTOR, 'input[placeholder="Select Month"]')
    _apply_button = (By.ID, 'apply_button')
    _search_button = (By.ID, 'search_button')

    # --- Actions ---
    def dismiss_login_if_present(self):
        try:
            popup_wait = WebDriverWait(self.driver, 4)
            element = popup_wait.until(EC.element_to_be_clickable(self._login_modal_close))
            element.click()
        except Exception:
            try:
                background_element = self.driver.find_element(*self._modal_overlay)
                background_element.click()
            except Exception:
                pass

    def navigate_to_cruise_section(self):
        """Navigates to the cruise section using a JavaScript click to bypass overlay panels."""
        # Wait for the element to be present and visible in the DOM
        element = self.wait.until(EC.visibility_of_element_located(self._cruise_nav_icon))
        
        # Bypasses physical coordinate rendering to click the DOM element directly
        self.driver.execute_script("arguments[0].click();", element)

    def select_destination(self, destination_name):
        """Clicks the placeholder box naturally and targets options via data-testid."""
        time.sleep(2) 
        element = self.wait.until(EC.element_to_be_clickable(self._destination_trigger))
        element.click()
        
        target_xpath = f'//li[@data-testid="{destination_name}"]'
        option_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
        option_element.click()

    def select_travel_month(self, month_name):
        """Picks the target month naturally from the open grid by slicing the first 3 letters."""
        element = self.wait.until(EC.element_to_be_clickable(self._month_trigger))
        element.click()
        time.sleep(1) # Allow calendar animation fade-in to complete

        # Converts "July" -> "Jul" to match the exact div text string in your DOM snapshot
        short_month = month_name[:3].capitalize()
        
        # Target the exact font-weight div tag inside the grid option cell card
        target_xpath = f'//div[contains(@style, "font-weight") and text()="{short_month}"]'
        
        month_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, target_xpath)))
        month_element.click()

        # Explicitly click the Apply button to collapse the calendar overlay safely
        apply_btn_element = self.wait.until(EC.element_to_be_clickable(self._apply_button))
        apply_btn_element.click()
        time.sleep(1)

    def click_search(self):
        """Clicks search, naturally shifts driver context to the newly opened results tab, and prints out available cruise listings."""
        # 1. Record our current primary window handle identity
        original_window = self.driver.current_window_handle
        
        # 2. Trigger the search button naturally
        element = self.wait.until(EC.element_to_be_clickable(self._search_button))
        element.click()
        
        # 3. Dynamic wait until the browser register opens a secondary tab window handles array
        self.wait.until(lambda d: len(d.window_handles) > 1)
        
        # 4. Filter handles list array and jump into the new window context
        all_windows = self.driver.window_handles
        for window_handle in all_windows:
            if window_handle != original_window:
                self.driver.switch_to.window(window_handle)
                print(f"[INFO] Successfully moved selenium focus window. New Tab URL: {self.driver.current_url}")
                break

        # 5. UI Elements synchronization layout on the new page results view
        # We target common MakeMyTrip cruise card listing title components
        _cruise_card_titles = (By.XPATH, '//div[contains(@class, "cruiseCard")]//h3|//p[contains(@class, "cruiseName")]|//div[contains(@class, "shipDetail")]/h3')
        
        try:
            # Let the listings fully render on screen
            time.sleep(5) 
            self.wait.until(EC.presence_of_element_located(_cruise_card_titles))
            cruise_elements = self.driver.find_elements(*_cruise_card_titles)
            
            print(f"\n==================== FOUND {len(cruise_elements)} AVAILABLE CRUISES ====================")
            for index, cruise in enumerate(cruise_elements, 1):
                name = cruise.text.strip()
                if name:
                    print(f"{index}. {name}")
            print("=========================================================================\n")
            
        except Exception as e:
            print(f"[WARNING] Could not parse individual cruise card title structures text details. Error: {str(e)}")
            # Fallback: Print what's inside the text layout structure if class names differ slightly
            print("[INFO] Fallback print - Page Title is currently: ", self.driver.title)

    