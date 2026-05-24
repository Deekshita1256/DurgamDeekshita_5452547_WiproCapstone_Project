from selenium.webdriver.common.by import By

class CruiseLocators:
    # Top Menu / Tab Navigation
    CRUISE_TAB = (By.XPATH, "//a[contains(@href, '/cruise')]|//span[contains(@class, 'chCruise')]")
    
    # Dropdown Selection Triggers
    SAILING_FROM_TRIGGER = (By.ID, 'destinationCity')
    DEPARTURE_MONTH_TRIGGER = (By.CSS_SELECTOR, 'input[placeholder="Select Month"]')
    DURATION_TRIGGER = (By.XPATH, "//span[text()='Duration']")
    CRUISE_LINE_TRIGGER = (By.XPATH, "//span[text()='Cruise Line']")
    
    # Dynamic Dropdown Options (Base templates for formatting)
    # Use these by replacing '{}' with the actual text value inside your Page methods
    SAILING_FROM_OPTION = (By.XPATH, "//ul[contains(@class, 'travelForPopup')]//span[text()='{}']")
    DEPARTURE_MONTH_OPTION = (By.XPATH, "//ul[contains(@class, 'travelForPopup')]//span[contains(text(), '{}')]")
    DURATION_OPTION = (By.XPATH, "//ul[contains(@class, 'travelForPopup')]//span[contains(text(), '{}')]")
    CRUISE_LINE_OPTION = (By.XPATH, "//ul[contains(@class, 'travelForPopup')]//span[contains(text(), '{}')]")
    
    # Search Trigger
    SEARCH_BUTTON = (By.XPATH, "//button[@id='search_button']")
    
    # Search Results Elements
    CRUISE_LIST_CONTAINER = (By.XPATH, "//div[contains(@class, 'cruiseListingCard')]")
    VIEW_CABINS_BUTTONS = (By.XPATH, '(//button[contains(@class, "section-sailing-date-btn") or contains(., "Dates")])[1]')