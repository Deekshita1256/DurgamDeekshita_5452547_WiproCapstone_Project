import time
from behave import given, when, then
from utils.excel_reader import ExcelReader
from pages.cruise_page import CruisePage
from pages.cabin_selection_page import CabinSelectionPage
from pages.partner_cruise_page import PartnerCruisePage
from pages.passenger_details_page import PassengerDetailsPage
from pages.payment_page import PaymentPage
from selenium.common.exceptions import UnexpectedAlertPresentException

# @given('the user has navigated to the Cruise module tab')
# def step_impl(context):
#     # Instantiate all Page Objects into the Behave runner context
#     context.cruise_page = CruisePage(context.driver)
#     context.cabin_page = CabinSelectionPage(context.driver)
#     context.partner_page = PartnerCruisePage(context.driver)
#     context.passenger_page = PassengerDetailsPage(context.driver)
#     context.payment_page = PaymentPage(context.driver)
    
#     # Execute action
#     context.cruise_page.navigate_to_cruises()

@when('the user searches for cruises using criteria from data sheet "{sheet_name}"')
def step_impl(context, sheet_name):
    # 🎯 READING SEARCH DATA FROM EXCEL: Destination and Month
    search_criteria = ExcelReader.read_excel("cruise_data.xlsx", sheet_name)[0]
    destination = search_criteria["Destination"]
    month = search_criteria["Month"]
    
    # Pass excel data straight to your pages
    context.cruise_page.select_sailing_from(destination)
    context.cruise_page.select_departure_month(month)
    context.cruise_page.click_search()

@when('the user selects the first available cruise listing card from the search results')
def step_impl(context):
    # Get a list of all currently open window tabs
    all_windows = context.driver.window_handles
    
    # If a new tab popped open, switch to the latest one (index -1)
    if len(all_windows) > 1:
        context.driver.switch_to.window(all_windows[-1])
        # Allow a brief moment for the heavy JavaScript components on the results page to render
        import time
        time.sleep(3) 
    
    # Now execute your scrolling and locator hunting safely!
    context.cruise_page.select_first_cruise()

@when('the user reviews cabin deals using traveler ages from data sheet "{sheet_name}"')
def step_impl(context, sheet_name):
    # 1. Read age criteria parameters from Excel
    age_records = ExcelReader.read_excel("cruise_data.xlsx", sheet_name)
    first_row_ages = age_records[0] if age_records else {"Age1": 28, "Age2": 32}
    
    # 2. Inject age properties directly into the inputs
    print(f"📥 Injecting passenger ages: Guest 1 ({first_row_ages['Age1']}), Guest 2 ({first_row_ages['Age2']})")
    context.partner_page.fill_passenger_ages_and_continue(
        first_row_ages["Age1"], 
        first_row_ages["Age2"]
    )
    
    # 3. Finalize cabin category choice and room checkout selections
    print("🛏️ Proceeding to cabin tier selections...")
    context.cabin_page.book_first_category_deal()
    context.cabin_page.handle_deposit_popup_if_present()
    context.cabin_page.select_final_stateroom()

@when('the user populates traveler registration forms using details from data sheet "{sheet_name}"')
def step_impl(context, sheet_name):
    # 🎯 READING PASSENGER NAMES FROM EXCEL
    search_criteria = ExcelReader.read_excel("cruise_data.xlsx", sheet_name)[0]
    
    p1_info = {
            "title": search_criteria.get("Passenger1Title", "Mr."),
            "gender": search_criteria.get("Passenger1Gender", "Male"),
            "first_name": search_criteria.get("Passenger1FirstName", "John"),
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
    
    context.passenger_page.fill_all_passenger_details(p1_info, p2_info)
    context.passenger_page.click_passenger_details_continue()
    context.passenger_page.select_dinner_and_proceed_to_payment()

@when('the user provides contact details from data sheet "{sheet_name}" to progress')
def step_impl(context, sheet_name):
    # 🎯 READING CONTACT FROM EXCEL
    search_criteria = ExcelReader.read_excel("cruise_data.xlsx", sheet_name)[0]
    
    email = search_criteria["ContactEmail"]
    phone = search_criteria["ContactPhone"]
    
    context.passenger_page.fill_contact_details(email, phone)
    context.passenger_page.click_contact_details_continue()
    context.passenger_page.select_dinner_and_proceed_to_payment()

@then('the user should view the final booking confirmation summary or payment gateway screen')
def step_impl(context):
    # 1. READ PAN CARD DATA FROM EXCEL & EXECUTE FINAL SUBMISSION
    search_criteria = ExcelReader.read_excel("cruise_data.xlsx", "SearchCriteria")[0]
    pan_card = search_criteria["PanCardNumber"]
    
    context.payment_page.fill_pan_and_complete_booking(pan_card)
    
    # ──────────────────────────────────────────────────────────────────
    # 🌟 ADDING ASSERTION 1: Verify the Page URL state is correct
    # ──────────────────────────────────────────────────────────────────
    current_url = context.driver.current_url.lower()
    print(f"[DEBUG] Current Gateway URL: {current_url}")
    
    assert "checkout" in current_url or "payment" in current_url or "booking" in current_url, \
        f"❌ Test Failed! Browser did not reach the payment gateway page. Current URL: {context.driver.current_url}"

    # 2. CAPTURE RENDERED TEXT OUT OF THE BILLING DASHBOARD
    total_due = context.payment_page.get_payment_total_due()
    print(f"[INFO] Total due captured from UI: {total_due}")

    # # ──────────────────────────────────────────────────────────────────
    # # 🌟 ADDING ASSERTION 2: Verify the Pricing Field isn't empty or zero
    # # ──────────────────────────────────────────────────────────────────
    # # This ensures the MakeMyTrip backend successfully calculated a live fare matrix
    # assert total_due is not None, "❌ Test Failed! Total Due element was not found or returned None."
    # assert len(total_due).strip() > 0, "❌ Test Failed! Total Due field is blank on the payment screen."
    
    # # Optional advanced verification: If total_due looks like "₹54,320", ensure it's not "0"
    # assert "0" not in total_due or total_due.strip() != "0", "❌ Test Failed! Booking summary shows a total due of 0."

    # print(f"[SUCCESS] E2E Test Passed & Validated! Data verified perfectly from Excel. Total due: {total_due}")