import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class PartnerCruisePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

    # --- Locators ---
    _show_dates_btn = (By.XPATH, '(//button[contains(@class, "section-sailing-date-btn") or contains(., "Dates")])[1]')
    _show_details_btn = (By.CSS_SELECTOR, 'button[data-ody-id="CruiseResultsBookButton"]')
    
    # Guest Inputs from image_7e79d7.jpg & image_7e7a8b.jpg
    _guest1_age_input = (By.CSS_SELECTOR, 'input[data-ody-id="GuestAge_0"]')
    _guest2_age_input = (By.CSS_SELECTOR, 'input[data-ody-id="GuestAge_1"]')
    
    # Continue button from image_7e7dd1.jpg
    _continue_btn = (By.XPATH, 
                     '//*[@id="packageDetails"]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/guest-info-v2/form/div[2]/div[2]/div/button/span')

    def select_first_listing_deal(self):
        """Scrolls down, clicks Show Dates, and then clicks Show Details using JS."""
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        
        show_dates = self.wait.until(EC.presence_of_element_located(self._show_dates_btn))
        self.driver.execute_script("arguments[0].click();", show_dates)
        time.sleep(2)
        
        self.driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(2)
        
        show_details = self.wait.until(EC.element_to_be_clickable(self._show_details_btn))
        self.driver.execute_script("arguments[0].click();", show_details)
        time.sleep(3)

    def fill_passenger_ages_and_continue(self, age1, age2):
        """Fills passenger ages, forces a page scroll, and triggers a clean DOM click."""
        g1_input = self.wait.until(EC.visibility_of_element_located(self._guest1_age_input))
        g2_input = self.wait.until(EC.visibility_of_element_located(self._guest2_age_input))
        
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
        continue_element = self.wait.until(EC.presence_of_element_located(self._continue_btn))
        
        # 3. Use an underlying JavaScript script trigger to execute the click action 
        # This safely cuts straight through the overlapping chat widget layout graphic!
        self.driver.execute_script("arguments[0].click();", continue_element)
        time.sleep(5)

    def get_top_cruise_title(self):
        

        print("[INFO] Scraping the top visible cruise listing title...")
        time.sleep(2) # Ensure cards are fully rendered
        
        # Target the main structural header text of the first card row
        top_card_title_element = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "(//span[contains(@class, 'text-gradient') or contains(@class, 'cruise-title')])[1]")
        ))
        title_text = top_card_title_element.text.strip()
        print(f"[INFO] Initial Top Cruise Title: '{title_text}'")
        return title_text

    def select_sort_by_departure_date(self):
        

        print("[INFO] Opening Sort By dropdown wrapper...")
        # Click the active Select2 sort selection container box
        sort_dropdown = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(@class, 'select2-selection') or contains(@id, 'select2')]")
        ))
        sort_dropdown.click()
        time.sleep(1.5)  # Let the absolute list overlay container open completely

        print("[INFO] Clicking the 'Departure Date' option...")
        # 🎯 BULLETPROOF MATCH: Handles the random server-side characters safely!
        departure_date_option = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@id, '-departureDate') or contains(text(), 'Departure Date')]")
        ))
        
        self.driver.execute_script("arguments[0].click();", departure_date_option)
        print("[INFO] Selection completed. Waiting for results grid refresh...")
        time.sleep(6)  # Give the AJAX loader ample time to replace the grid listings