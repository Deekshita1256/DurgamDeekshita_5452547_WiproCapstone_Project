import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from locators.passenger_details_locators import PassengerDetailsLocators
from selenium.webdriver.common.action_chains import ActionChains

class PassengerDetailsPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

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
        
        title1 = self.wait.until(EC.presence_of_element_located(PassengerDetailsLocators.P1_TITLE_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title1)
        time.sleep(1)
        
        self._safe_select_title(title1, p1_data["title"])
        Select(self.driver.find_element(*PassengerDetailsLocators.P1_GENDER_SELECT)).select_by_visible_text(p1_data["gender"])
        self.driver.find_element(*PassengerDetailsLocators.P1_FIRST_NAME_INPUT).send_keys(p1_data["first_name"])
        self.driver.find_element(*PassengerDetailsLocators.P1_LAST_NAME_INPUT).send_keys(p1_data["last_name"])
        
        Select(self.driver.find_element(*PassengerDetailsLocators.P1_DOB_MONTH_SELECT)).select_by_visible_text(p1_data["dob_month"])
        Select(self.driver.find_element(*PassengerDetailsLocators.P1_DOB_DAY_SELECT)).select_by_visible_text(str(p1_data["dob_day"]))
        Select(self.driver.find_element(*PassengerDetailsLocators.P1_DOB_YEAR_SELECT)).select_by_visible_text(str(p1_data["dob_year"]))

        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 350);")
        time.sleep(1.5)
        
        title2 = self.wait.until(EC.presence_of_element_located(PassengerDetailsLocators.P2_TITLE_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", title2)
        time.sleep(1)
        
        self._safe_select_title(title2, p2_data["title"])
        Select(self.driver.find_element(*PassengerDetailsLocators.P2_GENDER_SELECT)).select_by_visible_text(p2_data["gender"])
        self.driver.find_element(*PassengerDetailsLocators.P2_FIRST_NAME_INPUT).send_keys(p2_data["first_name"])
        self.driver.find_element(*PassengerDetailsLocators.P2_LAST_NAME_INPUT).send_keys(p2_data["last_name"])
        
        Select(self.driver.find_element(*PassengerDetailsLocators.P2_DOB_MONTH_SELECT)).select_by_visible_text(p2_data["dob_month"])
        Select(self.driver.find_element(*PassengerDetailsLocators.P2_DOB_DAY_SELECT)).select_by_visible_text(str(p2_data["dob_day"]))
        Select(self.driver.find_element(*PassengerDetailsLocators.P2_DOB_YEAR_SELECT)).select_by_visible_text(str(p2_data["dob_year"]))
        time.sleep(1)
        # """Scrolls down deeply and populates Passenger 1 and Passenger 2 forms."""
        # self.driver.execute_script("window.scrollBy(0, 400);")
        # time.sleep(1.5)
        
        # first_names = self.wait.until(EC.presence_of_all_elements_located(PassengerDetailsLocators.FIRST_NAME_INPUT))
        # last_names = self.driver.find_elements(*PassengerDetailsLocators.LAST_NAME_INPUT)
        
        # if first_names:
        #     first_names[0].send_keys(p1_data["first_name"])
        #     last_names[0].send_keys(p1_data["last_name"])
            
        # if len(first_names) > 1:
        #     first_names[1].send_keys(p2_data["first_name"])
        #     last_names[1].send_keys(p2_data["last_name"])

    def click_passenger_details_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(PassengerDetailsLocators.P_DETAILS_CONTINUE_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)

        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(4) 

    def fill_contact_details(self, email, phone):
        email_field = self.wait.until(EC.presence_of_element_located(PassengerDetailsLocators.EMAIL_INPUT))
        phone_field = self.driver.find_element(*PassengerDetailsLocators.PHONE_INPUT)
        email_field.clear()
        email_field.send_keys(email)
        phone_field.clear()
        phone_field.send_keys(phone)

    def click_contact_details_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(PassengerDetailsLocators.CONTACT_CONTINUE_BTN))
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(3)

        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(5)

    def select_dinner_and_proceed_to_payment(self):
        """Selects dinner seating preferences using JavaScript to bypass hidden elements, 

            then triggers the checkout transition."""
        
        # 1. Locate the dining element structure safely
        dining_element = self.wait.until(EC.presence_of_element_located(PassengerDetailsLocators.DINING_SELECT))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dining_element)
        time.sleep(1)
        
        # 🔥 FIX: Instead of Select(dropdown).select_by_index(1), use JavaScript to force the selection!
        print("[INFO] Setting dining preference via DOM value injection...")
        self.driver.execute_script(
            "arguments[0].selectedIndex = 1; "
            "arguments[0].dispatchEvent(new Event('change'));", 
            dining_element
        )
        time.sleep(2)
        
        # 2. Extract and focus onto the exact Engine Redirect button seen in DevTools
        payment_btn = self.wait.until(EC.presence_of_element_located(PassengerDetailsLocators.PAYMENT_CONTINUE_BTN))
        
        # Scroll down explicitly to ensure any sticky summaries don't obstruct the element area
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", payment_btn)
        time.sleep(1)
        self.driver.execute_script("window.scrollBy(0, 150);")
        time.sleep(1)
        
        # 3. Fire the action using your Action Chain loop / JS fallback
        try:
            print("[INFO] Attempting native interaction chain click on redirect button.")
            actions = ActionChains(self.driver)
            actions.move_to_element(payment_btn).click().perform()
        except Exception:
            print("[WARNING] Click intercepted. Executing DOM dispatch fallback.")
            self.driver.execute_script("arguments[0].click();", payment_btn)

        # 4. Wait for the check-out section to process
        print("[INFO] Handoff initiated. Waiting for page state transition...")
        WebDriverWait(self.driver, 15).until(
            lambda d: "checkout" in d.current_url.lower() or "payment" in d.current_url.lower()
        )
        time.sleep(4)

    def is_first_name_error_displayed(self) -> bool:
        """Checks if the error text box element is physically visible on the screen."""
        try:
            error_element = self.driver.find_element(*PassengerDetailsLocators.ERROR_MESSAGE_TEXT)
            return error_element.is_displayed()
        except Exception:
            return False

    def get_review_grand_total(self):
        # Explicitly wait until the text inside the element is no longer empty
        from selenium.webdriver.support.ui import WebDriverWait
        
        # Self.GRAND_TOTAL_LOCATOR represents your locator (By.CLASS_NAME, "latoBlack")
        WebDriverWait(self.driver, 15).until(lambda d: d.find_element(*PassengerDetailsLocators.GRAND_TOTAL_LOCATOR).text.strip() != "")
        return self.driver.find_element(*PassengerDetailsLocators.GRAND_TOTAL_LOCATOR).text.strip()