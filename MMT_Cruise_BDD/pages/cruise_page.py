import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.cruise_locators import CruiseLocators
from selenium.webdriver.common.by import By

class CruisePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

        # 🌟 Your custom modal locators added here
        self._login_modal_close = (By.CSS_SELECTOR, 'span[data-cy="closeModal"]')
        self._modal_overlay = (By.CSS_SELECTOR, 'li[data-cy="account"]')
        self._cruise_tab = (By.CSS_SELECTOR, ".menu_Cruises")
        self._apply_button = (By.ID, 'apply_button')
        self._show_details_btn = (By.CSS_SELECTOR, 'button[data-ody-id="CruiseResultsBookButton"]')

    def dismiss_login_if_present(self):
        """Dismisses the modal overlay popup if it interrupts the view."""
        try:
            popup_wait = WebDriverWait(self.driver, 5) # Let it wait briefly for the modal to animate in
            element = popup_wait.until(EC.element_to_be_clickable(self._login_modal_close))
            element.click()
        except Exception:
            try:
                background_element = self.driver.find_element(*self._modal_overlay)
                background_element.click()
            except Exception:
                pass # If it's not there, proceed safely

    def navigate_to_cruises(self):
        """Clicks on the Cruise tab on the MakeMyTrip main menu."""
        cruise_tab = self.wait.until(EC.element_to_be_clickable(CruiseLocators.CRUISE_TAB))
        cruise_tab.click()
        time.sleep(2)  # Allow page to transition to the cruise engine

    def select_sailing_from(self, city_name):
        """Opens the 'Sailing From' dropdown and selects the specified city."""
        self.wait.until(EC.element_to_be_clickable(CruiseLocators.SAILING_FROM_TRIGGER)).click()
        
        # Format the dynamic XPATH with our city variable
        target_xpath = f'//li[@data-testid="{city_name}"]'
        option_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, target_xpath)))
        option_element.click()

    def select_departure_month(self, month_year):
        """Opens the 'Departure Month' dropdown and selects the specified month/year."""
        self.wait.until(EC.element_to_be_clickable(CruiseLocators.DEPARTURE_MONTH_TRIGGER)).click()
        
         # Converts "July" -> "Jul" to match the exact div text string in your DOM snapshot
        short_month = month_year[:3].capitalize()
        
        # Target the exact font-weight div tag inside the grid option cell card
        target_xpath = f'//div[contains(@style, "font-weight") and text()="{short_month}"]'
        
        month_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, target_xpath)))
        month_element.click()

        # Explicitly click the Apply button to collapse the calendar overlay safely
        apply_btn_element = self.wait.until(EC.element_to_be_clickable(self._apply_button))
        apply_btn_element.click()
        time.sleep(1)

    def select_duration(self, duration_text):
        """Opens the 'Duration' dropdown and selects the matching option."""
        self.wait.until(EC.element_to_be_clickable(CruiseLocators.DURATION_TRIGGER)).click()
        
        dynamic_xpath = (CruiseLocators.DURATION_OPTION[0], 
                         CruiseLocators.DURATION_OPTION[1].format(duration_text))
        
        self.wait.until(EC.element_to_be_clickable(dynamic_xpath)).click()

    def select_cruise_line(self, cruise_line_name):
        """Opens the 'Cruise Line' dropdown and selects the matching option."""
        self.wait.until(EC.element_to_be_clickable(CruiseLocators.CRUISE_LINE_TRIGGER)).click()
        
        dynamic_xpath = (CruiseLocators.CRUISE_LINE_OPTION[0], 
                         CruiseLocators.CRUISE_LINE_OPTION[1].format(cruise_line_name))
        
        self.wait.until(EC.element_to_be_clickable(dynamic_xpath)).click()

    def click_search(self):
        """Clicks the central Search button."""
        self.wait.until(EC.element_to_be_clickable(CruiseLocators.SEARCH_BUTTON)).click()
        time.sleep(3)  # Wait for results to load

    def verify_results_appear(self):
        """Returns True if cruise options are loaded on the results list."""
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(CruiseLocators.CRUISE_LIST_CONTAINER))
            return len(elements) > 0
        except:
            return False

    def select_first_cruise(self):
        
        """Scrolls down, clicks Show Dates, and then clicks Show Details using JS."""
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        
        show_dates = self.wait.until(EC.presence_of_element_located(CruiseLocators.VIEW_CABINS_BUTTONS))
        self.driver.execute_script("arguments[0].click();", show_dates)
        time.sleep(2)
        
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        
        show_details = self.wait.until(EC.element_to_be_clickable(self._show_details_btn))
        self.driver.execute_script("arguments[0].click();", show_details)
        time.sleep(3)