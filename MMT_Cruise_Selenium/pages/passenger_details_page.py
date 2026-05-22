import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class PassengerDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    # --- PASSENGER 1 LOCATORS ---
    _p1_title_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_Title"]')
    _p1_gender_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_GenderSEL"]')
    _p1_first_name_input = (By.CSS_SELECTOR, 'input[id*="TravelerAccount_1_FirstName"]')
    _p1_last_name_input = (By.CSS_SELECTOR, 'input[id*="TravelerAccount_1_LastName"]')
    _p1_dob_month_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_DateUC_Month"]')
    _p1_dob_day_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_DateUC_Day"]')
    _p1_dob_year_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_DateUC_Year"]')

    # --- PASSENGER 2 LOCATORS ---
    _p2_title_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_Title"]')
    _p2_gender_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_GenderSEL"]')
    _p2_first_name_input = (By.CSS_SELECTOR, 'input[id*="TravelerAccount_2_FirstName"]')
    _p2_last_name_input = (By.CSS_SELECTOR, 'input[id*="TravelerAccount_2_LastName"]')
    _p2_dob_month_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_DateUC_Month"]')
    _p2_dob_day_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_DateUC_Day"]')
    _p2_dob_year_select = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_DateUC_Year"]')

    # --- CONTACT INFO LOCATORS ---
    # 🟢 Using partial match 'contains' CSS selectors here to avoid dynamic prefix failures
    _email_input = (By.CSS_SELECTOR, 'input[id*="BookingContact_EMail"]')
    _phone_input = (By.CSS_SELECTOR, 'input[id*="BookingContact_Phone1_Number"]')

    # --- DISTINCT STEP BUTTON LOCATORS ---
    _p_details_continue_btn = (By.ID, 'PessengerContinue')
    _contact_continue_btn = (By.XPATH, '//*[@id="st-accordion"]/div[2]/div/div[2]/input')

    
    # Corrected partial id from DevTools: id="_ctl0_MainContentsPH__ctl0_DiningPrefSEL"
    _dining_select = (By.CSS_SELECTOR, 'select[id*="DiningPrefSEL"]')
    
    # Final Payment Submission Button
    _payment_continue_btn = (By.ID, "_ctl0_MainContentsPH__ctl0_BookAndRedirectBTN")

    # 🎯 Captured from your screenshot's highlighted HTML block:
    _first_name_error_msg = (By.XPATH, "//div[contains(@id, 'PaxErrorBox')]")
        
        # The first name input field (showing the red error border in your screenshot)
    _first_name_input = (By.XPATH, "//input[@placeholder='First Name' or contains(@id, 'FirstName')]")


    _grand_total_locator = (By.XPATH, "//span[contains(@class, 'latoBlack') and contains(text(), '₹')]")


    def _safe_select_title(self, element, preferred_text):
        """Helper method to select title dropdown options safely."""
        select_obj = Select(element)
        try:
            select_obj.select_by_visible_text(preferred_text)
        except Exception:
            try:
                clean_text = preferred_text.replace(".", "")
                select_obj.select_by_visible_text(clean_text)
            except Exception:
                print(f"[WARNING] Title text '{preferred_text}' not found. Defaulting to index 1.")
                select_obj.select_by_index(1)

    def fill_all_passenger_details(self, p1_data, p2_data):
        """Scrolls down deeply and populates Passenger 1 and Passenger 2 forms."""
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(1.5)
        
        title1 = self.wait.until(EC.presence_of_element_located(self._p1_title_select))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title1)
        time.sleep(1)
        
        self._safe_select_title(title1, p1_data["title"])
        Select(self.driver.find_element(*self._p1_gender_select)).select_by_visible_text(p1_data["gender"])
        self.driver.find_element(*self._p1_first_name_input).send_keys(p1_data["first_name"])
        self.driver.find_element(*self._p1_last_name_input).send_keys(p1_data["last_name"])
        
        Select(self.driver.find_element(*self._p1_dob_month_select)).select_by_visible_text(p1_data["dob_month"])
        Select(self.driver.find_element(*self._p1_dob_day_select)).select_by_visible_text(str(p1_data["dob_day"]))
        Select(self.driver.find_element(*self._p1_dob_year_select)).select_by_visible_text(str(p1_data["dob_year"]))

        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(1.5)
        
        title2 = self.wait.until(EC.presence_of_element_located(self._p2_title_select))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title2)
        time.sleep(1)
        
        self._safe_select_title(title2, p2_data["title"])
        Select(self.driver.find_element(*self._p2_gender_select)).select_by_visible_text(p2_data["gender"])
        self.driver.find_element(*self._p2_first_name_input).send_keys(p2_data["first_name"])
        self.driver.find_element(*self._p2_last_name_input).send_keys(p2_data["last_name"])
        
        Select(self.driver.find_element(*self._p2_dob_month_select)).select_by_visible_text(p2_data["dob_month"])
        Select(self.driver.find_element(*self._p2_dob_day_select)).select_by_visible_text(str(p2_data["dob_day"]))
        Select(self.driver.find_element(*self._p2_dob_year_select)).select_by_visible_text(str(p2_data["dob_year"]))
        time.sleep(1)

    def click_passenger_details_continue(self):
        """Clicks the <button> element after entering passenger profiles."""
        continue_btn = self.wait.until(EC.presence_of_element_located(self._p_details_continue_btn))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
        time.sleep(1)
        
        self.driver.execute_script("arguments[0].click();", continue_btn)
        time.sleep(4) 

    def fill_contact_details(self, email, phone):
        """Natively targets fields directly via explicit wait conditions."""
        email_field = self.wait.until(EC.visibility_of_element_located(self._email_input))
        email_field.clear()
        email_field.send_keys(email)
        
        phone_field = self.wait.until(EC.visibility_of_element_located(self._phone_input))
        phone_field.clear()
        phone_field.send_keys(phone)
        time.sleep(1)

    def click_contact_details_continue(self):
        """Clicks the <a> link element to finish the contact detail sub-step cleanly."""
        continue_btn = self.wait.until(EC.presence_of_element_located(self._contact_continue_btn))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
        time.sleep(1)
        
        self.driver.execute_script("arguments[0].click();", continue_btn)
        time.sleep(5)

    def select_dinner_and_proceed_to_payment(self):
        """Selects dinner seating preferences, forces scrolling, 
        and hits the precise engine button to transition pages."""
        from selenium.webdriver.common.action_chains import ActionChains
        
        # 1. Handle the dinner dropdown layout context safely
        dining_element = self.wait.until(EC.presence_of_element_located(self._dining_select))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dining_element)
        time.sleep(1)
        
        dropdown = Select(dining_element)
        dropdown.select_by_index(1)  
        time.sleep(2)
        
        # 2. Extract and focus onto the exact Engine Redirect button seen in DevTools
        payment_btn = self.wait.until(EC.presence_of_element_located(self._payment_continue_btn))
        
        # Scroll down explicitly to ensure any sticky summaries don't obstruct the element area
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_btn)
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 150);")
        time.sleep(1)
        
        # 3. Fire the action using an explicit Action Chain loop
        # ... (Keep your working scroll and action chain click code from before) ...

        try:
            print("[INFO] Attempting native interaction chain click on redirect button.")
            actions = ActionChains(self.driver)
            actions.move_to_element(payment_btn).click().perform()
        except Exception:
            print("[WARNING] Click intercepted. Executing DOM dispatch fallback.")
            self.driver.execute_script("arguments[0].click();", payment_btn)

        # UPDATED: Wait for the check-out section to process instead of forcing a hard domain switch
        print("[INFO] Handoff initiated. Waiting for page state transition...")
        WebDriverWait(self.driver, 15).until(
            lambda d: "checkout" in d.current_url.lower() or "payment" in d.current_url.lower()
        )
        time.sleep(4)  # Let the payment fields settle down completely

    def get_first_name_error_message(self) -> str:
        """Checks for the presence of the first name error message and returns its text."""
        try:
            error_element = self.driver.find_element(*self._first_name_error_msg)
            if error_element.is_displayed():
                return error_element.text.strip()
        except Exception:
            pass
        return ""
    
    def get_review_grand_total(self):
        # Explicitly wait until the text inside the element is no longer empty
        from selenium.webdriver.support.ui import WebDriverWait
        
        # Self._grand_total_locator represents your locator (By.CLASS_NAME, "latoBlack")
        WebDriverWait(self.driver, 15).until(lambda d: d.find_element(*self._grand_total_locator).text.strip() != "")
        return self.driver.find_element(*self._grand_total_locator).text.strip()