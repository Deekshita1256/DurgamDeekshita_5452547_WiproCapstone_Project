from selenium.webdriver.common.by import By

class PassengerDetailsLocators:

    # --- PASSENGER 1 LOCATORS ---
    P1_TITLE_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_Title"]')
    P1_GENDER_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_GenderSEL"]')
    P1_FIRST_NAME_INPUT = (By.CSS_SELECTOR, 'input[id*="TravelerAccount_1_FirstName"]')
    P1_LAST_NAME_INPUT = (By.CSS_SELECTOR, 'input[id*="TravelerAccount_1_LastName"]')
    P1_DOB_MONTH_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_DateUC_Month"]')
    P1_DOB_DAY_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_DateUC_Day"]')
    P1_DOB_YEAR_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_1_DateUC_Year"]')

    # --- PASSENGER 2 LOCATORS ---
    P2_TITLE_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_Title"]')
    P2_GENDER_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_GenderSEL"]')
    P2_FIRST_NAME_INPUT = (By.CSS_SELECTOR, 'input[id*="TravelerAccount_2_FirstName"]')
    P2_LAST_NAME_INPUT = (By.CSS_SELECTOR, 'input[id*="TravelerAccount_2_LastName"]')
    P2_DOB_MONTH_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_DateUC_Month"]')
    P2_DOB_DAY_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_DateUC_Day"]')
    P2_DOB_YEAR_SELECT = (By.CSS_SELECTOR, 'select[id*="TravelerAccount_2_DateUC_Year"]')

    # --- CONTACT INFO LOCATORS ---
    EMAIL_INPUT = (By.CSS_SELECTOR, 'input[id*="BookingContact_EMail"]')
    PHONE_INPUT = (By.CSS_SELECTOR, 'input[id*="BookingContact_Phone1_Number"]')

    # --- DISTINCT STEP BUTTON LOCATORS ---
    P_DETAILS_CONTINUE_BTN = (By.ID, 'PessengerContinue')
    CONTACT_CONTINUE_BTN = (By.XPATH, '//*[@id="st-accordion"]/div[2]/div/div[2]/input')

    # --- DINING PREFERENCE LOCATORS ---
    DINING_SELECT = (By.CSS_SELECTOR, 'select[id*="DiningPrefSEL"]')

# --- FINAL PAYMENT SUBMISSION LOCATORS ---
    PAYMENT_CONTINUE_BTN = (By.ID, "_ctl0_MainContentsPH__ctl0_BookAndRedirectBTN")

    # Header Validation
    REVIEW_BOOKING_HEADER = (By.XPATH, "//h2[contains(text(), 'Review Booking') or contains(text(), 'Traveler')]")
    
    # Traveler Section Containers
    TRAVELER_ROW_CONTAINER = (By.XPATH, "//div[contains(@class, 'travelerDetails')]")
    

    
    # Validation / Error Elements
    ERROR_MESSAGE_TEXT = (By.XPATH, "//div[contains(@id, 'PaxErrorBox')]")
    
    # Proceed to Next Step
    PROCEED_TO_PAYMENT_BUTTON = (By.XPATH, "//button[contains(text(), 'Proceed to Payment') or contains(text(), 'Continue')]")

    GRAND_TOTAL_LOCATOR = (By.XPATH, "//span[contains(@class, 'latoBlack') and contains(text(), '₹')]")
