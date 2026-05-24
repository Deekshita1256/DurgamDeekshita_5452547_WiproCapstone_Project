from selenium.webdriver.common.by import By

class PaymentLocators:

    #Payment locators
    PAN_INPUT = (By.CSS_SELECTOR, "input[data-cy='InputField'][placeholder='ENTER PAN']")
    COMPLETE_BOOKING_BTN = (By.XPATH, "//*[@id='proceedToPaymentDiv']/p/button")
    FINAL_BOOKING_BTN = (By.XPATH, "//button[@data-testid='proceed-to-payment-btn']")

    # Page Title / Gateway Verification
    PAYMENT_PAGE_HEADER = (By.XPATH, "//h2[contains(text(), 'Payment Options') or contains(text(), 'Make Payment')]")
    
    # Available Payment Options List
    PAYMENT_METHODS_LIST = (By.XPATH, "//ul[contains(@class, 'paymentMethods')]/li")
    
    # Common Payment Mode Triggers
    CREDIT_DEBIT_CARD_TAB = (By.XPATH, "//span[contains(text(), 'Credit/Debit') or contains(text(), 'Card')]")
    NET_BANKING_TAB = (By.XPATH, "//span[contains(text(), 'Net Banking')]")
    UPI_TAB = (By.XPATH, "//span[contains(text(), 'UPI')]")
    
    # Summary Fields for assertions
    FINAL_PAYABLE_AMOUNT = (By.XPATH, "//p[contains(text(), 'Total Due')]/following-sibling::p//span[contains(text(), '₹')] | //span[contains(@class, 'PriceText') or contains(text(), '1,05,552')]")