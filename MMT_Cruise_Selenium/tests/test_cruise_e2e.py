import pytest
import allure
from utils.excel_reader import ExcelReader 
from pages.cruise_page import CruisePage
from pages.partner_cruise_page import PartnerCruisePage
from pages.cabin_selection_page import CabinSelectionPage
from pages.passenger_details_page import PassengerDetailsPage
from pages.payment_page import PaymentPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_search_criteria():
    """Reads primary booking, contact information, and payment data from 'SearchCriteria' sheet."""
    records = ExcelReader.read_excel("cruise_data.xlsx", "SearchCriteria")
    return records[0] if records else {}

def get_passenger_ages():
    """Reads multiple variations of guest ages from 'PassengerAges' sheet for parameterization."""
    raw_data = ExcelReader.read_excel("cruise_data.xlsx", "PassengerAges")
    return [(row["Age1"], row["Age2"]) for row in raw_data if row["Age1"] is not None]


@allure.feature("Cruise Booking Module")
@allure.story("End to End Cruise Selection and Checkout Reservation Flow")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("guest1_age, guest2_age", get_passenger_ages())
def test_cruise_search_and_passenger_details_e2e(driver, guest1_age, guest2_age):
    
    # --- PHASE 0: EXTRACT DATA FROM EXCEL ---
    with allure.step("Extracting primary search parameters and customer registration values from Excel"):
        excel_data = get_search_criteria()
        
        destination = excel_data.get("Destination", "Asia and Asia Pacific")
        travel_month = excel_data.get("Month", "July")
        
        # Build structured records for passenger details
        p1_info = {
            "title": excel_data.get("Passenger1Title", "Mr."),
            "gender": excel_data.get("Passenger1Gender", "Male"),
            "first_name": excel_data.get("Passenger1FirstName", "John"),
            "last_name": excel_data.get("Passenger1LastName", "Doe"),
            "dob_month": excel_data.get("Passenger1DOBMonth", "Jan"),
            "dob_day": int(float(excel_data.get("Passenger1DOBDay", 15))),
            "dob_year": int(float(excel_data.get("Passenger1DOBYear", 1988)))
        }
        
        p2_info = {
            "title": excel_data.get("Passenger2Title", "Mrs."),
            "gender": excel_data.get("Passenger2Gender", "Female"),
            "first_name": excel_data.get("Passenger2FirstName", "Jane"),
            "last_name": excel_data.get("Passenger2LastName", "Doe"),
            "dob_month": excel_data.get("Passenger2DOBMonth", "May"),
            "dob_day": int(float(excel_data.get("Passenger2DOBDay", 20))),
            "dob_year": int(float(excel_data.get("Passenger2DOBYear", 1990)))
        }
        
        email = excel_data.get("ContactEmail", "automation_test@example.com")
        phone = excel_data.get("ContactPhone", "9876543210")
        pan_card = excel_data.get("PanCardNumber", "ABCDE1234F")

        # Attach runtime metadata to Allure layout
        allure.attach(f"Destination: {destination}\nMonth: {travel_month}\nGuest 1 Age Input: {guest1_age}\nGuest 2 Age Input: {guest2_age}", 
                      name="Excel Core Parameters Info", attachment_type=allure.attachment_type.TEXT)
        
        allure.dynamic.description(f"E2E Parameterized Execution for {destination} during {travel_month}. Guest Ages: {guest1_age}, {guest2_age}")

    # --- PHASE 1: MAKEMYTRIP NAVIGATION ---
    cruise_page = CruisePage(driver)
    
    with allure.step("Navigating to MakeMyTrip home landing page"):
        # Corrected: Explicit navigation removed because your conftest.py driver fixture 
        # already automatically reads config.properties and opens the base_url for you!
        cruise_page.dismiss_login_if_present()
        
    with allure.step("Accessing the Cruise module section"):
        cruise_page.navigate_to_cruise_section()
        current_url = driver.current_url.lower()
        assert "/cruise" in current_url, f"❌ Failed to reach Cruise landing page. URL: {driver.current_url}"
        allure.attach(driver.get_screenshot_as_png(), name="Cruise Landing Screen", attachment_type=allure.attachment_type.PNG)
    
    with allure.step(f"Selecting Destination option: '{destination}'"):
        cruise_page.select_destination(destination)
        
    with allure.step(f"Selecting Travel Month: '{travel_month}' and hitting Apply"):
        cruise_page.select_travel_month(travel_month)
        search_btn = driver.find_element(*cruise_page._search_button)
        assert search_btn.is_displayed(), "❌ Calendar overlay failed to close cleanly."
        
    with allure.step("Clicking on Search Button to generate partner redirect handles"):
        initial_window_count = len(driver.window_handles)
        cruise_page.click_search()
        final_window_count = len(driver.window_handles)
        assert final_window_count > initial_window_count, f"❌ Redirect failed to open a new tab."
        assert "odysol.com" in driver.current_url, f"❌ Focus failed to switch to partner domain. URL: {driver.current_url}"

    # --- PHASE 2: PARTNER AGES VALIDATION ---
    partner_page = PartnerCruisePage(driver)
    
    with allure.step("Selecting primary cruise package listing card"):
        partner_page.select_first_listing_deal()
        allure.attach(driver.get_screenshot_as_png(), name="Expanded Package Form View", attachment_type=allure.attachment_type.PNG)
        
    with allure.step(f"Submitting parameterized age criteria (Guest1: {guest1_age}, Guest2: {guest2_age})"):
        partner_page.fill_passenger_ages_and_continue(guest1_age, guest2_age)
        allure.attach(driver.get_screenshot_as_png(), name="Ages Verification Form Completed", attachment_type=allure.attachment_type.PNG)

    # --- PHASE 3: CABIN AND CATEGORY SELECTION ---
    cabin_page = CabinSelectionPage(driver)

    with allure.step("Selecting primary choice from Category list"):
        cabin_page.book_first_category_deal()
        
    with allure.step("Handling dynamic non-refundable warning pop-up if present"):
        cabin_page.handle_deposit_popup_if_present()
        
    with allure.step("Confirming final explicit Stateroom configuration layout option"):
        cabin_page.select_final_stateroom()
        allure.attach(driver.get_screenshot_as_png(), name="Final Cabin Booking Confirmed", attachment_type=allure.attachment_type.PNG)
        assert "checkout" in driver.current_url.lower() or "booking" in driver.current_url.lower(), f"❌ Failed to reach Passenger Checkout page."

    # --- PHASE 4: PASSENGER REGISTRATION FORM ENTRY ---
    passenger_page = PassengerDetailsPage(driver)

    with allure.step("Filling out registration names and birthdays for Passenger 1 and Passenger 2"):
        passenger_page.fill_all_passenger_details(p1_info, p2_info)

    with allure.step("Submitting passenger registration details to open contact block step"):
        passenger_page.click_passenger_details_continue()

    with allure.step("Populating contact information fields"):
        passenger_page.fill_contact_details(email, phone)
        allure.attach(driver.get_screenshot_as_png(), name="Populated Contact Info Step", attachment_type=allure.attachment_type.PNG)

    with allure.step("Submitting contact details to proceed to dinner slot configuration"):
        passenger_page.click_contact_details_continue()

    with allure.step("Selecting dinner seating slot preference and moving forward"):
        passenger_page.select_dinner_and_proceed_to_payment()
        allure.attach(driver.get_screenshot_as_png(), name="Dinner Seating Applied Screen", attachment_type=allure.attachment_type.PNG)

    # --- PHASE 5: PAYMENT GATEWAY VERIFICATION ---
    payment_page = PaymentPage(driver)

    with allure.step("Entering PAN Card authentication number and completing booking hold request"):
        payment_page.fill_pan_and_complete_booking(pan_card)
        allure.attach(driver.get_screenshot_as_png(), name="Final Booking Step Execution Status", attachment_type=allure.attachment_type.PNG)

        # Final Verification Milestone Assertion
        WebDriverWait(driver, 30).until(
            lambda d: "review" not in d.current_url.lower()
        )