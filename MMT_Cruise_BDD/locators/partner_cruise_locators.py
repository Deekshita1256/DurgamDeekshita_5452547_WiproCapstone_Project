from selenium.webdriver.common.by import By

class PartnerCruiseLocators:
    # Page Context and Validation
    PARTNER_PAGE_HEADER = (By.XPATH, "//h1 | //h2[contains(@class, 'heading') or contains(text(), 'Cruise')]")
    
    # Booking Actions
    CONTINUE_BOOKING_BUTTON = (By.XPATH, 
                     '//*[@id="packageDetails"]/div/div[3]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/guest-info-v2/form/div[2]/div[2]/div/button/span')
    SHOW_DATES_BUTTON = (By.XPATH, '(//button[contains(@class, "section-sailing-date-btn") or contains(., "Dates")])[1]')
    BOOK_NOW_BUTTON = (By.XPATH, "//a[contains(text(), 'Book Now') or contains(@class, 'bookNowBtn')]")
    
    # Pricing summaries or terms often found on partner transition pages
    PRICE_DETAILS_SIDEBAR = (By.XPATH, "//div[contains(@class, 'priceDetails') or contains(@class, 'fareSummary')]")
    GUEST_AGE1_INPUT = (By.CSS_SELECTOR, 'input[data-ody-id="GuestAge_0"]')
    GUEST_AGE2_INPUT = (By.CSS_SELECTOR, 'input[data-ody-id="GuestAge_1"]')

    #Titles 
    CRUISE_TITLE = (By.XPATH, "(//span[contains(@class, 'text-gradient') or contains(@class, 'cruise-title')])[1]")

    # Sort By Dropdown
    SORT_BY_DROPDOWN = (By.XPATH, "//span[contains(@class, 'select2-selection') or contains(@id, 'select2')]")
    DEPARTURE_DATE_OPTION = (By.XPATH, "//li[contains(@id, '-departureDate') or contains(text(), 'Departure Date')]")