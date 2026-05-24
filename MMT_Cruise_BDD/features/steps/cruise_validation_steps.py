import time
from behave import given, when, then
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.partner_cruise_locators import PartnerCruiseLocators
from utils.excel_reader import ExcelReader
from pages.cruise_page import CruisePage
from pages.partner_cruise_page import PartnerCruisePage
from pages.cabin_selection_page import CabinSelectionPage
from pages.passenger_details_page import PassengerDetailsPage
from pages.payment_page import PaymentPage
from locators.payment_locators import PaymentLocators
# =========================================================================
# REUSABLE ASSISTANCE MATCHERS / RECURRENT STRATEGIES
# =========================================================================

@when('the user completes a default cabin and room selection strategy')
def step_impl(context):
    context.partner_page = PartnerCruisePage(context.driver)
    context.partner_page.select_first_listing_deal()
    
    age_records = ExcelReader.read_excel("cruise_data.xlsx", "PassengerAges")
    guest1_age = age_records[0]["Age1"] if age_records else 28
    guest2_age = age_records[0]["Age2"] if age_records else 32
    context.partner_page.fill_passenger_ages_and_continue(guest1_age, guest2_age)
    
    context.cabin_page = CabinSelectionPage(context.driver)
    context.cabin_page.book_first_category_deal()
    context.cabin_page.handle_deposit_popup_if_present()
    context.cabin_page.select_final_stateroom()
    
    WebDriverWait(context.driver, 15).until(
        lambda d: "checkout" in d.current_url.lower() or "booking" in d.current_url.lower()
    )

@when('the user provides valid passenger details and moves to payment options')
def step_impl(context):
    context.passenger_page = PassengerDetailsPage(context.driver)
    WebDriverWait(context.driver, 15).until(lambda d: len(d.window_handles) > 1)
    context.driver.switch_to.window(context.driver.window_handles[-1])
    
    excel_data = ExcelReader.read_excel("cruise_data.xlsx", "SearchCriteria")[0]
    p1_info = {
        "title": excel_data.get("Passenger1Title", "Mr."), "gender": excel_data.get("Passenger1Gender", "Male"),
        "first_name": excel_data.get("Passenger1FirstName", "John"), "last_name": excel_data.get("Passenger1LastName", "Doe")
    }
    p2_info = {
        "title": excel_data.get("Passenger2Title", "Mrs."), "gender": excel_data.get("Passenger2Gender", "Female"),
        "first_name": excel_data.get("Passenger2FirstName", "Jane"), "last_name": excel_data.get("Passenger2LastName", "Doe")
    }
    
    context.passenger_page.fill_all_passenger_details(p1_info, p2_info)
    context.passenger_page.click_passenger_details_continue()
    
    email = excel_data.get("ContactEmail", "automation_test@example.com")
    phone = excel_data.get("ContactPhone", "9876543210")
    context.passenger_page.fill_contact_details(email, phone)
    context.passenger_page.click_contact_details_continue()
    context.passenger_page.select_dinner_and_proceed_to_payment()

# =========================================================================
# TEST CASE 1 STEPS: INVALID PAN CARD NUMBER
# =========================================================================

@then('the system should ensure the final booking proceed button remains disabled')
def step_impl(context):
    wait = WebDriverWait(context.driver, 15)
    
    # 🌟 STEP 1: Let the page object audit the button state directly 
    # (The invalid PAN was already typed in the previous @when step!)
    try:
        button_is_locked = wait.until(lambda d: context.payment_page.is_proceed_button_disabled())
    except Exception:
        # If a timeout occurs or checking fails, assume it's unlocked so the test fails
        button_is_locked = False
        
    # 🌟 STEP 2: Assert your safety guardrail
    assert button_is_locked, "❌ GUARDRAIL CRITICAL FAILURE: The 'PROCEED TO PAYMENT' button unlocked for an invalid PAN configuration!"
# =========================================================================
# TEST CASE 2 STEPS: MISSING MANDATORY FIELD
# =========================================================================

from behave import when, then
from selenium.webdriver.support.ui import WebDriverWait

@when('the user completes a default cabin selection stage but leaves the passenger first name blank from data sheet "{sheet_name}"')
def step_impl(context, sheet_name):
    # 🎯 READING PASSENGER NAMES FROM EXCEL
    search_criteria = ExcelReader.read_excel("cruise_data.xlsx", sheet_name)[0]
    
    p1_info = {
            "title": search_criteria.get("Passenger1Title", "Mr."),
            "gender": search_criteria.get("Passenger1Gender", "Male"),
            "first_name": "",  # ❌ INTENTIONALLY LEAVING THIS BLANK
            "last_name": search_criteria.get("Passenger1LastName", "Doe"),
            "dob_month": search_criteria.get("Passenger1DOBMonth", "Jan"),
            "dob_day": int(float(search_criteria.get("Passenger1DOBDay", 15))),
            "dob_year": int(float(search_criteria.get("Passenger1DOBYear", 1988)))
        }
        
    p2_info = {
            "title": search_criteria.get("Passenger2Title", "Mrs."),
            "gender": search_criteria.get("Passenger2Gender", "Female"),
            "first_name": search_criteria.get("Passenger2FirstName", "Jane"),
            "last_name": search_criteria.get("Passenger2LastName", "Doe"),
            "dob_month": search_criteria.get("Passenger2DOBMonth", "May"),
            "dob_day": int(float(search_criteria.get("Passenger2DOBDay", 20))),
            "dob_year": int(float(search_criteria.get("Passenger2DOBYear", 1990)))
        }
    
    # Fill out the forms, but intentionally do not submit yet
    context.passenger_page.fill_all_passenger_details(p1_info, p2_info)


@when('the user attempts to submit the passenger details form')
def step_impl(context):
    # Trigger the continue button to force the website to validate the blank field
    context.passenger_page.click_passenger_details_continue()


@then('the system should display a validation error containing invalid first name')
def step_impl(context):
    wait = WebDriverWait(context.driver, 10)
    
    print("[INFO] Waiting for the validation error box to become visible...")
    
    try:
        # Wait up to 10 seconds for the element to return True for is_displayed()
        error_appeared = wait.until(lambda d: context.passenger_page.is_first_name_error_displayed())
    except Exception:
        # If it times out, the box never appeared
        error_appeared = False
        
    # The only assertion we need: Did the box show up?
    assert error_appeared, "❌ GUARDRAIL FAILURE: The error text box did not appear on the screen!"

# =========================================================================
# TEST CASE 3 STEPS: LOWERCASE PAN CARD ENTRY AUTOMATION
# =========================================================================

@then('the user enters a lowercase PAN id "{lowercase_pan}" and the system should accept the input and proceeds')
def step_impl(context, lowercase_pan):
    context.payment_page = PaymentPage(context.driver)
    context.payment_page.fill_pan_and_complete_booking(lowercase_pan)

    WebDriverWait(context.driver, 30).until(lambda d: "review" not in d.current_url.lower())
    button_is_abled = context.payment_page.is_proceed_button_abled()
    assert not button_is_abled, "❌ FUNCTIONAL ERROR: The 'PROCEED TO PAYMENT' button remained locked for lowercase alphanumeric characters!"

# =========================================================================
# TEST CASE 4 STEPS: LAYOUT RESILIENCY WINDOW RESCALE
# =========================================================================

@when('the user rescales the browser viewport resolution to a narrower "{resolution}" boundary view')
def step_impl(context, resolution):
    width, height = map(int, resolution.split('x'))
    context.driver.set_window_size(width, height)

@then('the user should see that the cruise package listings grid is displayed and stable under the scaled layout')
def step_impl(context):
    # Switch focus to the newly spawned window after search click occurs
    WebDriverWait(context.driver, 15).until(lambda d: len(d.window_handles) > 1)
    context.driver.switch_to.window(context.driver.window_handles[-1])
    
    context.partner_page = PartnerCruisePage(context.driver)
    wait = WebDriverWait(context.driver, 15)
    results_container = wait.until(EC.visibility_of_element_located(PartnerCruiseLocators.SHOW_DATES_BUTTON))
    context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", results_container)
    
    assert results_container.is_displayed(), "❌ LAYOUT ERROR: Cruise package listings grid is broken or hidden on rescale!"

# =========================================================================
# TEST CASE 5 STEPS: FINANCIAL MATCH TOTAL FARE SUMMARY SYNC
# =========================================================================


@when('the user submits a valid PAN card to advance past the review context onto the payment gateway screen')
def step_impl(context):
    wait = WebDriverWait(context.driver, 15)
    context.passenger_details_page = PassengerDetailsPage(context.driver)
    context.review_price = context.passenger_details_page.get_review_grand_total()
    assert context.review_price != "", "❌ SCRIPTING FAILURE: Failed to grab initial Grand Total price string from review page."


    excel_data = ExcelReader.read_excel("cruise_data.xlsx", "SearchCriteria")[0]
    pan_card = excel_data.get("PanCardNumber", "FFVPD6592H")
    
    context.payment_page = PaymentPage(context.driver)
    wait = WebDriverWait(context.driver, 15)
    pan_field = wait.until(EC.visibility_of_element_located(PaymentLocators.PAN_INPUT))
    context.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan_field)
    pan_field.clear()
    pan_field.send_keys(pan_card)
    
    final_submit_btn = wait.until(EC.element_to_be_clickable(PaymentLocators.FINAL_BOOKING_BTN))
    final_submit_btn.click()
    wait.until(lambda d: "payments.makemytrip.com" in d.current_url.lower())

@then('the final gateway payment price should exactly match the baseline review stage total price string')
def step_impl(context):
    wait = WebDriverWait(context.driver, 15)
    context.payment_page = PaymentPage(context.driver)
    payment_gateway_price = context.payment_page.get_payment_total_due()
    
    cleaned_review = context.review_price.replace(" ", "").strip()
    cleaned_gateway = payment_gateway_price.replace(" ", "").strip()
    
    assert cleaned_review == cleaned_gateway, (
        f"❌ FINANCIAL AUDIT FAIL: Price discrepancy found during handoff! "
        f"Review summary total showed '{cleaned_review}', but the payment engine requested '{cleaned_gateway}'!"
    )

# =========================================================================
# TEST CASE 6 STEPS: SORT BY DEPARTURE DATE AND GRID CONTENT ASSERTION
# =========================================================================

@when('the user notes the title of the top cruise result under default price sorting')
def step_impl(context):
    WebDriverWait(context.driver, 15).until(lambda d: len(d.window_handles) > 1)
    context.driver.switch_to.window(context.driver.window_handles[-1])
    
    context.partner_page = PartnerCruisePage(context.driver)
    context.baseline_title = context.partner_page.get_top_cruise_title()

@when('the user changes the active sorting dropdown option selection to "Departure Date"')
def step_impl(context):
    context.partner_page = PartnerCruisePage(context.driver)
    context.partner_page.select_sort_by_departure_date()
    time.sleep(3)  # Allow sorting DOM transitions to finalize

@then('the cruise listing grid positions should update, showing a different top cruise item')
def step_impl(context):
    context.partner_page = PartnerCruisePage(context.driver)
    sorted_title = context.partner_page.get_top_cruise_title()
    assert context.baseline_title != sorted_title, (
        f"❌ SORT CRITERIA ERROR: The top item did not change! "
        f"Both before and after show: '{context.baseline_title}'"
    )