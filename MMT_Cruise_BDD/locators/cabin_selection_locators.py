from selenium.webdriver.common.by import By

class CabinSelectionLocators:
    # Page Header/Validation Elements
    CRUISE_NAME_HEADER = (By.XPATH, "//h3[contains(@class, 'cruiseName')]")
    TOTAL_PRICE_SUMMARY = (By.XPATH, "//span[contains(@class, 'totalPrice')]")
    
    # Cabin Category Selection Tabs (e.g., Inside, Oceanview, Balcony, Suite)
    CABIN_CATEGORY_TABS = (By.XPATH, "//ul[contains(@class, 'cabinTabs')]/li")
    DYNAMIC_CATEGORY_TAB = (By.XPATH, "//ul[contains(@class, 'cabinTabs')]/li[contains(text(), '{}')]")
    
    # Book / Select Buttons
    SELECT_CABIN_BUTTONS = (By.XPATH, '//div[contains(@class, "modal-footer")]//a[contains(text(), "Continue") or contains(@onclick, "SubmitSelection")]')
    FIRST_AVAILABLE_CABIN_BOOK_BUTTON = (By.CSS_SELECTOR, 'a[data-ody-id="BookNowButton"]')
    FINAL_CONFIRM_BOOK_BUTTON = (By.CSS_SELECTOR, 'a[data-ody-id="StateroomBookNowButton"]')
    
    # Cabin Details / Overview Text
    CABIN_DESCRIPTION_TEXT = (By.XPATH, "//div[contains(@class, 'cabinDesc')]")