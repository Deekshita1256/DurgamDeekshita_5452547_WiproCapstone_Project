import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.partner_cruise_locators import PartnerCruiseLocators

class PartnerCruisePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    def select_first_listing_deal(self):
        """Scrolls down, clicks Show Dates, and then clicks Show Details using JS."""
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        
        show_dates = self.wait.until(EC.presence_of_element_located(PartnerCruiseLocators.SHOW_DATES_BUTTON))
        self.driver.execute_script("arguments[0].click();", show_dates)
        time.sleep(2)
        
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        
        show_details = self.wait.until(EC.element_to_be_clickable(PartnerCruiseLocators.BOOK_NOW_BUTTON))
        self.driver.execute_script("arguments[0].click();", show_details)
        time.sleep(3)

    def fill_passenger_ages_and_continue(self, age1, age2):

        """Fills passenger ages, forces a page scroll, and triggers a clean DOM click."""
        g1_input = self.wait.until(EC.visibility_of_element_located(PartnerCruiseLocators.GUEST_AGE1_INPUT))
        g2_input = self.wait.until(EC.visibility_of_element_located(PartnerCruiseLocators.GUEST_AGE2_INPUT))
        
        # Input Age Data
        g1_input.clear()
        g1_input.send_keys(str(int(float(age1))))
        g2_input.clear()
        g2_input.send_keys(str(int(float(age2))))
        time.sleep(1)
        
        # 1. Scroll window forcefully down to expose the button context area
        self.driver.execute_script("window.scrollBy(0, 400);")
        time.sleep(2)
        
        # 2. Wait for the corrected button selector to become present in DOM tree structure
        continue_element = self.wait.until(EC.presence_of_element_located(PartnerCruiseLocators.CONTINUE_BOOKING_BUTTON))
        
        # 3. Use an underlying JavaScript script trigger to execute the click action 
        # This safely cuts straight through the overlapping chat widget layout graphic!
        self.driver.execute_script("arguments[0].click();", continue_element)
        time.sleep(5)


        # """Fills passenger ages, forces a page scroll, and triggers a clean DOM click."""
        # # Using index maps or explicit references since locators are cleaned up
        # inputs = self.wait.until(EC.presence_of_all_elements_located(PartnerCruiseLocators.TERMS_CHECKBOX))
        # if len(inputs) >= 2:
        #     inputs[0].clear()
        #     inputs[0].send_keys(str(int(float(age1))))
        #     inputs[1].clear()
        #     inputs[1].send_keys(str(int(float(age2))))
        # time.sleep(1)
        
        # self.driver.execute_script("window.scrollBy(0, 400);")
        # time.sleep(2)
        
        # continue_btn = self.wait.until(EC.element_to_be_clickable(PartnerCruiseLocators.CONTINUE_BOOKING_BUTTON))
        # self.driver.execute_script("arguments[0].click();", continue_btn)
        # time.sleep(5)

    def get_top_cruise_title(self):

        print("[INFO] Scraping the top visible cruise listing title...")
        time.sleep(2) # Ensure cards are fully rendered
            
        # Target the main structural header text of the first card row
        top_card_title_element = self.wait.until(EC.presence_of_element_located(PartnerCruiseLocators.CRUISE_TITLE))
        title_text = top_card_title_element.text.strip()
        print(f"[INFO] Initial Top Cruise Title: '{title_text}'")
        return title_text
    
    def select_sort_by_departure_date(self):
        
        print("[INFO] Opening Sort By dropdown wrapper...")
        # Click the active Select2 sort selection container box
        sort_dropdown = self.wait.until(EC.element_to_be_clickable(PartnerCruiseLocators.SORT_BY_DROPDOWN))
        sort_dropdown.click()
        time.sleep(1.5)  # Let the absolute list overlay container open completely

        print("[INFO] Clicking the 'Departure Date' option...")
        # 🎯 BULLETPROOF MATCH: Handles the random server-side characters safely!
        departure_date_option = self.wait.until(EC.element_to_be_clickable(PartnerCruiseLocators.DEPARTURE_DATE_OPTION))
        
        self.driver.execute_script("arguments[0].click();", departure_date_option)
        print("[INFO] Selection completed. Waiting for results grid refresh...")
        time.sleep(6)  # Give the AJAX loader ample time to replace the grid listings