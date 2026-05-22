import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class PaymentPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    # --- Locators ---
    # PAN Card Verification Input
    _pan_input = (By.CSS_SELECTOR, "input[data-cy='InputField'][placeholder='ENTER PAN']")
    
    # Final Booking/Hold Button
    _complete_booking_btn = (By.XPATH, "//*[@id='proceedToPaymentDiv']/p/button")

    _final_booking_btn = (By.XPATH, "//button[@data-testid='proceed-to-payment-btn']")

   
    _payment_total_due = (By.XPATH, "//p[contains(text(), 'Total Due')]/following-sibling::p//span[contains(text(), '₹')] | //span[contains(@class, 'PriceText') or contains(text(), '1,05,552')]")

    def fill_pan_and_complete_booking(self, pan_card_number):
        """Types PAN, switches back to the primary brand window framework, 
        waits for validation logic to clear the disabled tag, and clicks."""
        
        # 1. Type the PAN into the input field
        pan_field = self.wait.until(EC.presence_of_element_located(self._pan_input))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan_field)
        time.sleep(1)
        
        pan_field.clear()
        pan_field.send_keys(pan_card_number)
        print(f"[INFO] Successfully entered PAN Card data.")
        
    
            
        # If Odysol was an iframe instead, use this line:
        # self.driver.switch_to.default_content()

        # 3. Explicitly wait for the 'disabled' attribute to disappear from the DOM
        print("[INFO] Waiting for UI validation to remove the 'disabled' lock...")
        final_submit_btn = self.wait.until(EC.presence_of_element_located(self._complete_booking_btn))
        
        # Force a scroll up to bring the button into view
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", final_submit_btn)
        time.sleep(1)
        
        # Custom wait condition: Wait until the 'disabled' attribute is removed completely
        self.wait.until(lambda d: d.find_element(*self._complete_booking_btn).get_attribute("disabled") is None)
        print("[INFO] Button lock cleared! Proceeding with final click interaction.")

        # 4. Fire the clean native click
        try:
            self.wait.until(EC.element_to_be_clickable(self._complete_booking_btn)).click()
            print("[SUCCESS] Final payment authorization button triggered.")
        except Exception:
            print("[WARNING] Click intercepted. Forcing native ActionChain sequence.")
            from selenium.webdriver.common.action_chains import ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element(final_submit_btn).click().perform()
            
        time.sleep(5)

    def is_proceed_button_disabled(self) -> bool:
        """
        Evaluates whether the 'PROCEED TO PAYMENT' button is actively disabled.
        Returns True if blocked, False if it remains active.
        """
        try:
            button_element = self.driver.find_element(*self._final_booking_btn)
            
            # Check 1: Verify native HTML 'disabled' attribute status
            if button_element.get_attribute("disabled") is not None:
                return True
                
            # Check 2: Verify if 'disabled' exists inside the class list string
            class_attr = button_element.get_attribute("class") or ""
            if "disabled" in class_attr.lower():
                return True
                
            # Check 3: Natively fallback check
            if not button_element.is_enabled():
                return True
                
        except Exception:
            pass
            
        return False
    
    def is_proceed_button_abled(self) -> bool:
        """
        Evaluates whether the 'PROCEED TO PAYMENT' button is actively disabled.
        Returns True if blocked, False if it remains active.
        """
        try:
            button_element = self.driver.find_element(*self._complete_booking_btn)
            
            # Check 1: Verify native HTML 'disabled' attribute status
            if button_element.get_attribute("disabled") is not None:
                return True
                
            # Check 2: Verify if 'disabled' exists inside the class list string
            class_attr = button_element.get_attribute("class") or ""
            if "disabled" in class_attr.lower():
                return True
                
            # Check 3: Natively fallback check
            if not button_element.is_enabled():
                return True
                
        except Exception:
            pass
            
        return False

    def wait_until_button_is_enabled(self, timeout=10):
        """Explicitly waits for the disabled attribute to drop from the DOM."""
        from selenium.webdriver.support.ui import WebDriverWait
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*self._final_booking_btn).get_attribute("disabled") is None
        )

        
    def get_payment_total_due(self) -> str:
        """Extracts the final total amount string loaded on the actual payment option gateway layout."""
        try:
            return self.driver.find_element(*self._payment_total_due).text.strip()
        except Exception:
            return ""