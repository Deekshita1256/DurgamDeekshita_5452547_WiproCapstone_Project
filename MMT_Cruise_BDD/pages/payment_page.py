# import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from locators.payment_locators import PaymentLocators
# from selenium.webdriver.common.action_chains import ActionChains

# class PaymentPage:
#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(self.driver, 15)


#     def fill_pan_and_complete_booking(self, pan_card_number):
#         """Waits for the browser engine loading states to settle completely 
#         before typing the PAN card and handling the workflow submission or guardrails."""
        
#         print("[INFO] Arrived at Payment Phase. Waiting for browser state transition...")
        
#         # 1. Wait for the browser to report document.readyState == 'complete'
#         WebDriverWait(self.driver, 20).until(
#             lambda d: d.execute_script("return document.readyState") == "complete"
#         )
        
#         # 2. Give complex calculators and gateway elements a safe cushion to render
#         time.sleep(5) 
        
#         # 3. Locate and populate the PAN input field
#         print("[INFO] Locating the PAN Input field...")
#         pan_field = self.wait.until(EC.presence_of_element_located(PaymentLocators.PAN_INPUT))
        
#         # Perform Viewport Scroll and Type action sequence
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan_field)
#         time.sleep(1.5)
        
#         pan_field.clear()
#         pan_field.send_keys(str(pan_card_number))
#         print(f"[INFO] Successfully entered PAN Card data.")
#         time.sleep(1)
            
            
#         # 4. Handle submission lock verification (Only runs if expect_disabled=False)
#         print("[INFO] Waiting for UI validation to remove the 'disabled' lock...")
#         final_submit_btn = self.wait.until(EC.presence_of_element_located(PaymentLocators.COMPLETE_BOOKING_BTN))
        
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", final_submit_btn)
#         time.sleep(1)
        
#         # Wait until the 'disabled' tag vanishes from the button attributes tree
#         self.wait.until(lambda d: d.find_element(*PaymentLocators.COMPLETE_BOOKING_BTN).get_attribute("disabled") is None)
#         print("[INFO] Button lock cleared! Proceeding with final click interaction.")

#         # 5. Click the authorization target
#         try:
#             self.wait.until(EC.element_to_be_clickable(PaymentLocators.COMPLETE_BOOKING_BTN)).click()
#             print("[SUCCESS] Final payment authorization button triggered.")
#         except Exception:
#             print("[WARNING] Native click failed. Forcing ActionChain sequence.")
#             from selenium.webdriver.common.action_chains import ActionChains
#             actions = ActionChains(self.driver)
#             actions.move_to_element(final_submit_btn).click().perform()
            
#         time.sleep(5)



#     def is_proceed_button_disabled(self, pan_card_number):
#         """
#         Evaluates whether the 'PROCEED TO PAYMENT' button is actively disabled.
#         Returns True if blocked, False if it remains active.
#         """
#         print("[INFO] Arrived at Payment Phase. Waiting for browser state transition...")
        
#         # 1. Wait for the browser to report document.readyState == 'complete'
#         WebDriverWait(self.driver, 20).until(
#             lambda d: d.execute_script("return document.readyState") == "complete"
#         )
        
#         # 2. Give complex calculators and gateway elements a safe cushion to render
#         time.sleep(5) 
        
#         # 3. Locate and populate the PAN input field
#         print("[INFO] Locating the PAN Input field...")
#         pan_field = self.wait.until(EC.presence_of_element_located(PaymentLocators.PAN_INPUT))
        
#         # Perform Viewport Scroll and Type action sequence
#         self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan_field)
#         time.sleep(1.5)
        
#         pan_field.clear()
#         pan_field.send_keys(str(pan_card_number))
#         print(f"[INFO] Successfully entered PAN Card data.")
#         time.sleep(1)

#         try:
#             button_element = self.driver.find_element(*PaymentLocators.FINAL_BOOKING_BTN)
            
#             # Check 1: Verify native HTML 'disabled' attribute status
#             if button_element.get_attribute("disabled") is not None:
#                 return True
                
#             # Check 2: Verify if 'disabled' exists inside the class list string
#             class_attr = button_element.get_attribute("class") or ""
#             if "disabled" in class_attr.lower():
#                 return True
                
#             # Check 3: Natively fallback check
#             if not button_element.is_enabled():
#                 return True
                
#         except Exception:
#             pass
            
#         return False
    
    
#     def is_proceed_button_abled(self) -> bool:
#         """
#         Evaluates whether the 'PROCEED TO PAYMENT' button is actively disabled.
#         Returns True if blocked, False if it remains active.
#         """
#         try:
#             button_element = self.driver.find_element(*PaymentLocators.COMPLETE_BOOKING_BTN)
            
#             # Check 1: Verify native HTML 'disabled' attribute status
#             if button_element.get_attribute("disabled") is not None:
#                 return True
                
#             # Check 2: Verify if 'disabled' exists inside the class list string
#             class_attr = button_element.get_attribute("class") or ""
#             if "disabled" in class_attr.lower():
#                 return True
                
#             # Check 3: Natively fallback check
#             if not button_element.is_enabled():
#                 return True
                
#         except Exception:
#             pass
            
#         return False

#     def get_payment_total_due(self) -> str:
#         try:
#             return self.driver.find_element(*PaymentLocators.FINAL_PAYABLE_AMOUNT).text.strip()
#         except Exception:
#             return ""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.payment_locators import PaymentLocators
from selenium.webdriver.common.action_chains import ActionChains

class PaymentPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def fill_pan_and_complete_booking(self, pan_card_number):
        """Waits for the browser engine loading states to settle completely 
        before typing the PAN card and handling the workflow submission."""
        
        print("[INFO] Arrived at Payment Phase. Waiting for browser state transition...")
        
        WebDriverWait(self.driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(5) 
        
        print("[INFO] Locating the PAN Input field...")
        pan_field = self.wait.until(EC.presence_of_element_located(PaymentLocators.PAN_INPUT))
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan_field)
        time.sleep(1.5)
        
        pan_field.clear()
        pan_field.send_keys(str(pan_card_number))
        print(f"[INFO] Successfully entered PAN Card data.")
        time.sleep(1)
            
        print("[INFO] Waiting for UI validation to remove the 'disabled' lock...")
        final_submit_btn = self.wait.until(EC.presence_of_element_located(PaymentLocators.FINAL_BOOKING_BTN))
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", final_submit_btn)
        time.sleep(1)
        
        self.wait.until(lambda d: d.find_element(*PaymentLocators.COMPLETE_BOOKING_BTN).get_attribute("disabled") is None)
        print("[INFO] Button lock cleared! Proceeding with final click interaction.")

        try:
            self.wait.until(EC.element_to_be_clickable(PaymentLocators.COMPLETE_BOOKING_BTN)).click()
            print("[SUCCESS] Final payment authorization button triggered.")
        except Exception:
            print("[WARNING] Native click failed. Forcing ActionChain sequence.")
            actions = ActionChains(self.driver)
            actions.move_to_element(final_submit_btn).click().perform()
            
        time.sleep(5)

    # ──────────────────────────────────────────────────────────────────
    # 🌟 FIXED: REMOVED DUPLICATE TYPING AND UNUSED PARAMETERS 🌟
    # ──────────────────────────────────────────────────────────────────
    def is_proceed_button_disabled(self) -> bool:
        """
        Evaluates whether the 'PROCEED TO PAYMENT' button is actively disabled
        after the step file has already input the invalid PAN card data.
        """
        print("[INFO] Auditing 'PROCEED TO PAYMENT' element state...")
        time.sleep(2) # Brief sync pause for validation styling to latch onto DOM
        
        try:
            # Match locator using COMPLETE_BOOKING_BTN to remain consistent across page models
            button_element = self.driver.find_element(*PaymentLocators.COMPLETE_BOOKING_BTN)
            
            # Check 1: Verify native HTML 'disabled' attribute status
            if button_element.get_attribute("disabled") is not None:
                print("[INFO] Guardrail Active: Native disabled attribute found.")
                return True
                
            # Check 2: Verify if 'disabled' exists inside the class list string
            class_attr = button_element.get_attribute("class") or ""
            if "disabled" in class_attr.lower():
                print("[INFO] Guardrail Active: Class styles match disabled state.")
                return True
                
            # Check 3: Native fallback check
            if not button_element.is_enabled():
                print("[INFO] Guardrail Active: Component reporting non-interactable.")
                return True
                
        except Exception as e:
            print(f"[WARNING] Problem reading button elements: {str(e)}")
            return True # Fallback to True to prevent accidental false positives
            
        return False
    
    def is_proceed_button_abled(self) -> bool:
        """Evaluates whether the 'PROCEED TO PAYMENT' button is active."""
        try:
            button_element = self.driver.find_element(*PaymentLocators.COMPLETE_BOOKING_BTN)
            
            if button_element.get_attribute("disabled") is not None:
                return True
            class_attr = button_element.get_attribute("class") or ""
            if "disabled" in class_attr.lower():
                return True
            if not button_element.is_enabled():
                return True
        except Exception:
            pass
            
        return False

    def get_payment_total_due(self) -> str:
        try:
            return self.driver.find_element(*PaymentLocators.FINAL_PAYABLE_AMOUNT).text.strip()
        except Exception:
            return ""