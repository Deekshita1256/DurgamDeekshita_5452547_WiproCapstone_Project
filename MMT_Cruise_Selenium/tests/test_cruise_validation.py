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
import time
from selenium.webdriver.common.by import By


def get_search_criteria():
    """Reads primary booking, contact information, and data models from Excel."""
    records = ExcelReader.read_excel("cruise_data.xlsx", "SearchCriteria")
    return records[0] if records else {}

def get_passenger_ages():
    """Reads multiple guest age configurations for parameterization runs."""
    raw_data = ExcelReader.read_excel("cruise_data.xlsx", "PassengerAges")
    return [(row["Age1"], row["Age2"]) for row in raw_data if row["Age1"] is not None]


@allure.feature("Cruise Booking Module - Input Guardrails")
class TestCruiseValidation:
    """Encapsulates all functional boundary and negative validation tests for the Cruise Module."""

    # =========================================================================
    # ❌ NEGATIVE TEST CASE 1: INVALID PAN CARD NUMBER
    # =========================================================================
    @allure.story("Negative Test - Invalid Short PAN Input Restriction Check")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("guest1_age, guest2_age", get_passenger_ages())
    def test_cruise_booking_invalid_pan_negative(self, driver, guest1_age, guest2_age):
        with allure.step("Extracting primary search parameters and customer data models from Excel"):
            excel_data = get_search_criteria()
            destination = excel_data.get("Destination", "Asia and Asia Pacific")
            travel_month = excel_data.get("Month", "July")
            
            p1_info = {
                "title": excel_data.get("Passenger1Title", "Mr."), "gender": excel_data.get("Passenger1Gender", "Male"),
                "first_name": excel_data.get("Passenger1FirstName", "John"), "last_name": excel_data.get("Passenger1LastName", "Doe"),
                "dob_month": excel_data.get("Passenger1DOBMonth", "Jan"), "dob_day": int(float(excel_data.get("Passenger1DOBDay", 15))), "dob_year": int(float(excel_data.get("Passenger1DOBYear", 1988)))
            }
            p2_info = {
                "title": excel_data.get("Passenger2Title", "Mrs."), "gender": excel_data.get("Passenger2Gender", "Female"),
                "first_name": excel_data.get("Passenger2FirstName", "Jane"), "last_name": excel_data.get("Passenger2LastName", "Doe"),
                "dob_month": excel_data.get("Passenger2DOBMonth", "May"), "dob_day": int(float(excel_data.get("Passenger2DOBDay", 20))), "dob_year": int(float(excel_data.get("Passenger2DOBYear", 1990)))
            }
            email = excel_data.get("ContactEmail", "automation_test@example.com")
            phone = excel_data.get("ContactPhone", "9876543210")

        cruise_page = CruisePage(driver)
        with allure.step("Handling home page initialization status"):
            cruise_page.dismiss_login_if_present()
        with allure.step("Accessing the Cruise module section"):
            cruise_page.navigate_to_cruise_section()
        with allure.step(f"Selecting Destination option: '{destination}'"):
            cruise_page.select_destination(destination)
        with allure.step(f"Selecting Travel Month: '{travel_month}' and applying filters"):
            cruise_page.select_travel_month(travel_month)
        with allure.step("Clicking on Search Button and verifying redirect handles"):
            initial_window_count = len(driver.window_handles)
            cruise_page.click_search()
            WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > initial_window_count)

        partner_page = PartnerCruisePage(driver)
        with allure.step("Selecting primary cruise package listing card"):
            partner_page.select_first_listing_deal()
        with allure.step("Submitting parameterized age criteria"):
            partner_page.fill_passenger_ages_and_continue(guest1_age, guest2_age)

        cabin_page = CabinSelectionPage(driver)
        with allure.step("Selecting primary choice from Category list"):
            cabin_page.book_first_category_deal()
            cabin_page.handle_deposit_popup_if_present()
            cabin_page.select_final_stateroom()
            WebDriverWait(driver, 15).until(lambda d: "checkout" in d.current_url.lower() or "booking" in d.current_url.lower())

        passenger_page = PassengerDetailsPage(driver)
        with allure.step("Filling out registration names and birthdays"):
            WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])
            passenger_page.fill_all_passenger_details(p1_info, p2_info)
        with allure.step("Submitting passenger registration details"):
            passenger_page.click_passenger_details_continue()
        with allure.step("Populating contact information fields"):
            passenger_page.fill_contact_details(email, phone)
        with allure.step("Submitting contact details to proceed"):
            passenger_page.click_contact_details_continue()
        with allure.step("Selecting dinner seating slot preference"):
            passenger_page.select_dinner_and_proceed_to_payment()

        payment_page = PaymentPage(driver)
        wait = WebDriverWait(driver, 15)
        with allure.step("Injecting an intentionally invalid short PAN number and validating button status"):
            pan_field = wait.until(EC.visibility_of_element_located(payment_page._pan_input))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan_field)
            pan_field.clear()
            pan_field.send_keys("ABC12")

            final_submit_btn = wait.until(EC.presence_of_element_located(payment_page._final_booking_btn))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", final_submit_btn)

            try:
                button_is_locked = wait.until(lambda d: payment_page.is_proceed_button_disabled())
            except Exception:
                button_is_locked = False

            allure.attach(driver.get_screenshot_as_png(), name="Disabled Button Verification State", attachment_type=allure.attachment_type.PNG)
            assert button_is_locked, "❌ GUARDRAIL CRITICAL FAILURE: The 'PROCEED TO PAYMENT' button unlocked for an invalid PAN configuration!"


    # =========================================================================
    # ❌ NEGATIVE TEST CASE 2: MISSING MANDATORY FIELD (New Code Added Below)
    # =========================================================================
    @allure.story("Negative Test - Missing Mandatory Field Guardrail Check")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("guest1_age, guest2_age", get_passenger_ages())
    def test_cruise_booking_missing_field_negative(self, driver, guest1_age, guest2_age):
        with allure.step("Extracting parameters and tampering data models to leave First Name blank"):
            excel_data = get_search_criteria()
            destination = excel_data.get("Destination", "Asia and Asia Pacific")
            travel_month = excel_data.get("Month", "July")
            
            p1_info = {
                "title": excel_data.get("Passenger1Title", "Mr."), "gender": excel_data.get("Passenger1Gender", "Male"),
                "first_name": "",  # ❌ INTENTIONALLY LEAVING THIS BLANK
                "last_name": excel_data.get("Passenger1LastName", "Doe"),
                "dob_month": excel_data.get("Passenger1DOBMonth", "Jan"), "dob_day": int(float(excel_data.get("Passenger1DOBDay", 15))), "dob_year": int(float(excel_data.get("Passenger1DOBYear", 1988)))
            }
            p2_info = {
                "title": excel_data.get("Passenger2Title", "Mrs."), "gender": excel_data.get("Passenger2Gender", "Female"),
                "first_name": excel_data.get("Passenger2FirstName", "Jane"), "last_name": excel_data.get("Passenger2LastName", "Doe"),
                "dob_month": excel_data.get("Passenger2DOBMonth", "May"), "dob_day": int(float(excel_data.get("Passenger2DOBDay", 20))), "dob_year": int(float(excel_data.get("Passenger2DOBYear", 1990)))
            }

        cruise_page = CruisePage(driver)
        with allure.step("Handling home page initialization status"):
            cruise_page.dismiss_login_if_present()
        with allure.step("Accessing the Cruise module section"):
            cruise_page.navigate_to_cruise_section()
        with allure.step(f"Selecting Destination option: '{destination}'"):
            cruise_page.select_destination(destination)
        with allure.step(f"Selecting Travel Month: '{travel_month}'"):
            cruise_page.select_travel_month(travel_month)
        with allure.step("Clicking on Search Button and verifying redirect"):
            initial_window_count = len(driver.window_handles)
            cruise_page.click_search()
            WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > initial_window_count)

        partner_page = PartnerCruisePage(driver)
        with allure.step("Selecting primary cruise package listing card"):
            partner_page.select_first_listing_deal()
        with allure.step("Submitting parameterized age criteria"):
            partner_page.fill_passenger_ages_and_continue(guest1_age, guest2_age)

        cabin_page = CabinSelectionPage(driver)
        with allure.step("Selecting room class and category specifications"):
            cabin_page.book_first_category_deal()
            cabin_page.handle_deposit_popup_if_present()
            cabin_page.select_final_stateroom()
            WebDriverWait(driver, 15).until(lambda d: "checkout" in d.current_url.lower() or "booking" in d.current_url.lower())

        passenger_page = PassengerDetailsPage(driver)
        wait = WebDriverWait(driver, 15)
        with allure.step("Filling out passenger details with the missing First Name field"):
            wait.until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])
            passenger_page.fill_all_passenger_details(p1_info, p2_info)

        with allure.step("Attempting to click continue and verifying error intercept guards"):
            passenger_page.click_passenger_details_continue()
            
            try:
                error_appeared = wait.until(lambda d: passenger_page.get_first_name_error_message() != "")
                captured_text = passenger_page.get_first_name_error_message()
            except Exception:
                error_appeared = False
                captured_text = ""

            allure.attach(driver.get_screenshot_as_png(), name="Missing Field Validation Error State", attachment_type=allure.attachment_type.PNG)

            # 🛑 VERIFICATION ASSERTIONS
            assert error_appeared, "❌ GUARDRAIL CRITICAL FAILURE: The application did not display an error message container when First Name was missing!"
            assert "Invalid First Name" in captured_text, f"❌ CONTENT MATCH FAILURE: Unexpected validation text style received: '{captured_text}'"
            
            print("[SUCCESS] Missing field guardrail verified successfully.")

   # =========================================================================
    # 🟢 POSITIVE TEST CASE 1: LOWERCASE PAN CARD ENTRY AUTOMATION
    # =========================================================================
    @allure.story("Positive Test 1 - Lowercase PAN Alphanumeric Input Handling")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("guest1_age, guest2_age", get_passenger_ages())
    def test_cruise_booking_lowercase_pan_positive(self, driver, guest1_age, guest2_age):
        with allure.step("Extracting primary search parameters and customer registration values from Excel"):
            excel_data = get_search_criteria()
            destination = excel_data.get("Destination", "Asia and Asia Pacific")
            travel_month = excel_data.get("Month", "July")
            
            p1_info = {
                "title": excel_data.get("Passenger1Title", "Mr."), "gender": excel_data.get("Passenger1Gender", "Male"),
                "first_name": excel_data.get("Passenger1FirstName", "John"), "last_name": excel_data.get("Passenger1LastName", "Doe"),
                "dob_month": excel_data.get("Passenger1DOBMonth", "Jan"), "dob_day": int(float(excel_data.get("Passenger1DOBDay", 15))), "dob_year": int(float(excel_data.get("Passenger1DOBYear", 1988)))
            }
            p2_info = {
                "title": excel_data.get("Passenger2Title", "Mrs."), "gender": excel_data.get("Passenger2Gender", "Female"),
                "first_name": excel_data.get("Passenger2FirstName", "Jane"), "last_name": excel_data.get("Passenger2LastName", "Doe"),
                "dob_month": excel_data.get("Passenger2DOBMonth", "May"), "dob_day": int(float(excel_data.get("Passenger2DOBDay", 20))), "dob_year": int(float(excel_data.get("Passenger2DOBYear", 1990)))
            }
            email = excel_data.get("ContactEmail", "automation_test@example.com")
            phone = excel_data.get("ContactPhone", "9876543210")

        cruise_page = CruisePage(driver)
        with allure.step("Handling home page initialization status"):
            cruise_page.dismiss_login_if_present()
        with allure.step("Accessing the Cruise module section"):
            cruise_page.navigate_to_cruise_section()
        with allure.step(f"Selecting Destination option: '{destination}'"):
            cruise_page.select_destination(destination)
        with allure.step(f"Selecting Travel Month: '{travel_month}'"):
            cruise_page.select_travel_month(travel_month)
        with allure.step("Clicking on Search Button and verifying redirect"):
            initial_window_count = len(driver.window_handles)
            cruise_page.click_search()
            WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > initial_window_count)

        partner_page = PartnerCruisePage(driver)
        with allure.step("Selecting primary cruise package listing card"):
            partner_page.select_first_listing_deal()
        with allure.step("Submitting parameterized age criteria"):
            partner_page.fill_passenger_ages_and_continue(guest1_age, guest2_age)

        cabin_page = CabinSelectionPage(driver)
        with allure.step("Selecting room class and category specifications"):
            cabin_page.book_first_category_deal()
            cabin_page.handle_deposit_popup_if_present()
            cabin_page.select_final_stateroom()
            WebDriverWait(driver, 15).until(lambda d: "checkout" in d.current_url.lower() or "booking" in d.current_url.lower())

        passenger_page = PassengerDetailsPage(driver)
        wait = WebDriverWait(driver, 15)
        with allure.step("Filling out passenger registration details"):
            wait.until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])
            passenger_page.fill_all_passenger_details(p1_info, p2_info)
        with allure.step("Submitting passenger details to open contact block"):
            passenger_page.click_passenger_details_continue()
        with allure.step("Populating contact information fields"):
            passenger_page.fill_contact_details(email, phone)
        with allure.step("Submitting contact details to proceed"):
            passenger_page.click_contact_details_continue()
        with allure.step("Selecting dinner seating slot preference and proceeding"):
            passenger_page.select_dinner_and_proceed_to_payment()

        payment_page = PaymentPage(driver)
        with allure.step("Entering PAN Card authentication number and completing booking hold request"):
            payment_page.fill_pan_and_complete_booking("ffvpd6592h")  # Intentionally lowercase to test case insensitivity
            allure.attach(driver.get_screenshot_as_png(), name="Final Booking Step Execution Status", attachment_type=allure.attachment_type.PNG)

            # Final Verification Milestone Assertion
            WebDriverWait(driver, 30).until(
                lambda d: "review" not in d.current_url.lower()
        )


            button_is_abled = payment_page.is_proceed_button_abled()
            allure.attach(driver.get_screenshot_as_png(), name="Lowercase PAN Button State", attachment_type=allure.attachment_type.PNG)

            # 🟢 The assertion checks that it is NOT disabled
            assert not button_is_abled, "❌ FUNCTIONAL ERROR: The 'PROCEED TO PAYMENT' button remained locked for lowercase alphanumeric characters!"
            print("[SUCCESS] Lowercase character transformation verification passed.")

    # =========================================================================
    # 🟢 POSITIVE TEST CASE 2: LAYOUT RESILIENCY WINDOW RESCALE (OPTIMIZED)
    # =========================================================================
    @allure.story("Positive Test 2 - UI Layout Resiliency Check on Window Rescale")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cruise_booking_responsive_rescale_positive(self, driver):
        """Validates layout container scaling right at the primary results search matrix."""
        
        with allure.step("Rescaling browser viewport resolution to a narrower 1024x768 boundary view"):
            driver.set_window_size(1024, 768)

        with allure.step("Extracting primary search parameters from Excel configuration source"):
            excel_data = get_search_criteria()
            destination = excel_data.get("Destination", "Asia and Asia Pacific")
            travel_month = excel_data.get("Month", "July")

        cruise_page = CruisePage(driver)
        with allure.step("Handling home page initialization status"):
            cruise_page.dismiss_login_if_present()
            
        with allure.step("Accessing the Cruise module section"):
            cruise_page.navigate_to_cruise_section()
            
        with allure.step(f"Selecting Destination option: '{destination}'"):
            cruise_page.select_destination(destination)
            
        with allure.step(f"Selecting Travel Month: '{travel_month}'"):
            cruise_page.select_travel_month(travel_month)
            
        with allure.step("Clicking on Search Button and waiting for the Results Tab shift transition"):
            initial_window_count = len(driver.window_handles)
            cruise_page.click_search()
            
            # Explicit sync verification tracking browser window multiplication rules
            WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > initial_window_count)
            driver.switch_to.window(driver.window_handles[-1])

        partner_page = PartnerCruisePage(driver)
        wait = WebDriverWait(driver, 15)
        
        with allure.step("Verifying Results Grid container visibility and element placement stability under scaled layout"):
            # Enforce synchronization against your listing container element on the page
            # Note: Replace `partner_page._first_deal_card` with the selector you use inside `select_first_listing_deal()`
            results_container = wait.until(EC.visibility_of_element_located(partner_page._show_dates_btn))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", results_container)
            
            # Responsive integrity validations
            assert results_container.is_displayed(), "❌ LAYOUT ERROR: Cruise package listings grid is broken or hidden on 1024x768 rescale!"
            
            allure.attach(driver.get_screenshot_as_png(), name="Listing Page 1024x768 Viewport State", attachment_type=allure.attachment_type.PNG)
            print("[SUCCESS] Responsive UI Rescale layout assertion verified early on the listing viewport grid.")

    # =========================================================================
    # 🟢 POSITIVE TEST CASE 3: FINANCIAL MATCH TOTAL FARE SUMMARY SYNC
    # =========================================================================
    @allure.story("Positive Test 3 - Dynamic Sidebar Total Fare Handoff Sync")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("guest1_age, guest2_age", get_passenger_ages())
    def test_cruise_booking_financial_price_sync_positive(self, driver, guest1_age, guest2_age):
        with allure.step("Extracting primary search parameters and customer registration values from Excel"):
            excel_data = get_search_criteria()
            destination = excel_data.get("Destination", "Asia and Asia Pacific")
            travel_month = excel_data.get("Month", "July")
            
            p1_info = {
                "title": excel_data.get("Passenger1Title", "Mr."), "gender": excel_data.get("Passenger1Gender", "Male"),
                "first_name": excel_data.get("Passenger1FirstName", "John"), "last_name": excel_data.get("Passenger1LastName", "Doe"),
                "dob_month": excel_data.get("Passenger1DOBMonth", "Jan"), "dob_day": int(float(excel_data.get("Passenger1DOBDay", 15))), "dob_year": int(float(excel_data.get("Passenger1DOBYear", 1988)))
            }
            p2_info = {
                "title": excel_data.get("Passenger2Title", "Mrs."), "gender": excel_data.get("Passenger2Gender", "Female"),
                "first_name": excel_data.get("Passenger2FirstName", "Jane"), "last_name": excel_data.get("Passenger2LastName", "Doe"),
                "dob_month": excel_data.get("Passenger2DOBMonth", "May"), "dob_day": int(float(excel_data.get("Passenger2DOBDay", 20))), "dob_year": int(float(excel_data.get("Passenger2DOBYear", 1990)))
            }
            email = excel_data.get("ContactEmail", "automation_test@example.com")
            phone = excel_data.get("ContactPhone", "9876543210")
            pan_card = excel_data.get("PanCardNumber", "ABCDE1234F")

        cruise_page = CruisePage(driver)
        with allure.step("Handling home page initialization status"):
            cruise_page.dismiss_login_if_present()
        with allure.step("Accessing the Cruise module section"):
            cruise_page.navigate_to_cruise_section()
        with allure.step(f"Selecting Destination option: '{destination}'"):
            cruise_page.select_destination(destination)
        with allure.step(f"Selecting Travel Month: '{travel_month}'"):
            cruise_page.select_travel_month(travel_month)
        with allure.step("Clicking on Search Button and verifying redirect"):
            initial_window_count = len(driver.window_handles)
            cruise_page.click_search()
            WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > initial_window_count)

        partner_page = PartnerCruisePage(driver)
        with allure.step("Selecting primary cruise package listing card"):
            partner_page.select_first_listing_deal()
        with allure.step("Submitting parameterized age criteria"):
            partner_page.fill_passenger_ages_and_continue(guest1_age, guest2_age)

        cabin_page = CabinSelectionPage(driver)
        with allure.step("Selecting room class and category specifications"):
            cabin_page.book_first_category_deal()
            cabin_page.handle_deposit_popup_if_present()
            cabin_page.select_final_stateroom()
            WebDriverWait(driver, 15).until(lambda d: "checkout" in d.current_url.lower() or "booking" in d.current_url.lower())

        passenger_page = PassengerDetailsPage(driver)
        wait = WebDriverWait(driver, 15)
        with allure.step("Filling out passenger registration details"):
            wait.until(lambda d: len(d.window_handles) > 1)
            driver.switch_to.window(driver.window_handles[-1])
            passenger_page.fill_all_passenger_details(p1_info, p2_info)
        with allure.step("Submitting passenger details to open contact block"):
            passenger_page.click_passenger_details_continue()
        with allure.step("Populating contact information fields"):
            passenger_page.fill_contact_details(email, phone)
        with allure.step("Submitting contact details to proceed"):
            passenger_page.click_contact_details_continue()
        with allure.step("Selecting dinner seating slot preference and proceeding"):
            passenger_page.select_dinner_and_proceed_to_payment()

        # 1. Scrape the baseline price amount on review screen before advancing
        with allure.step("Extracting baseline Grand Total price from the checkout review layout"):
            
            # ⏳ FIX: Explicitly wait until the grand total element text is populated and not blank
            # Note: Replace `passenger_page._grand_total_locator` with the actual locator variable defined inside your PassengerDetailsPage (e.g., self._grand_total_price)
            wait.until(lambda d: d.find_element(*passenger_page._grand_total_locator).text.strip() != "")
            
            # Now that we know the text has loaded, safely grab it
            review_price = passenger_page.get_review_grand_total() 
            print(f"[INFO] Baseline Review Stage Price Extracted: '{review_price}'")
            allure.attach(f"Review Price: {review_price}", name="Review Meta Log", attachment_type=allure.attachment_type.TEXT)
            
            assert review_price != "", "❌ SCRIPTING FAILURE: Failed to grab initial Grand Total price string from review page."


        payment_page = PaymentPage(driver)
        with allure.step("Entering valid PAN credentials and advancing past review context handles"):
            pan_field = wait.until(EC.visibility_of_element_located(payment_page._pan_input))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", pan_field)
            pan_field.clear()
            pan_field.send_keys(pan_card)
            
            final_submit_btn = wait.until(EC.element_to_be_clickable(payment_page._final_booking_btn))
            final_submit_btn.click()
            
            # Wait for handoff browser transitions onto payments.makemytrip.com endpoint
            wait.until(lambda d: "payments.makemytrip.com" in d.current_url.lower())

        # 2. Extract final gateway payment price and execute match verification
        with allure.step("Asserting exact price string match on the dynamic gateway landing screen"):
            wait.until(EC.visibility_of_element_located(payment_page._payment_total_due))
            payment_gateway_price = payment_page.get_payment_total_due() # Target structural label path sibling node
            
            print(f"[INFO] Handoff Payment Gateway Price Extracted: '{payment_gateway_price}'")
            allure.attach(driver.get_screenshot_as_png(), name="Payment Stage Verification Layout", attachment_type=allure.attachment_type.PNG)

            # Sanitize character spacing adjustments
            cleaned_review = review_price.replace(" ", "").strip()
            cleaned_gateway = payment_gateway_price.replace(" ", "").strip()

            # 🛑 VERIFICATION AUDIT ASSERTION
            assert cleaned_review == cleaned_gateway, (
                f"❌ FINANCIAL AUDIT FAIL: Price discrepancy found during handoff! "
                f"Review summary total showed '{cleaned_review}', but the payment engine requested '{cleaned_gateway}'!"
            )
            print("[SUCCESS] Financial matching auditing passed completely.")

    # =========================================================================
    # 🟢 POSITIVE TEST CASE 4: SORT BY DEPARTURE DATE AND GRID CONTENT ASSERTION
    # =========================================================================
    @allure.story("Positive Test 4 - Sort by Departure Date and Assert List Sorting Change")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cruise_booking_sort_by_departure_date_positive(self, driver):
        """Validates that sorting by Departure Date updates the position order of the search listings."""
        
        with allure.step("Extracting search criteria settings"):
            excel_data = get_search_criteria()
            destination = excel_data.get("Destination", "Asia and Asia Pacific")
            travel_month = excel_data.get("Month", "July")

        cruise_page = CruisePage(driver)
        with allure.step("Navigating to Cruise engine section"):
            cruise_page.dismiss_login_if_present()
            cruise_page.navigate_to_cruise_section()
            
        with allure.step("Running initial cruise search"):
            cruise_page.select_destination(destination)
            cruise_page.select_travel_month(travel_month)
            
            initial_window_count = len(driver.window_handles)
            cruise_page.click_search()
            
            # Switch context to the generated results window
            WebDriverWait(driver, 15).until(lambda d: len(d.window_handles) > initial_window_count)
            driver.switch_to.window(driver.window_handles[-1])

        partner_page = PartnerCruisePage(driver)

        # 1. Grab the baseline top cruise card title text (Sorted by Price)
        with allure.step("Capture the baseline top cruise title (Default: Price Sort)"):
            baseline_title = partner_page.get_top_cruise_title()

        # 2. Trigger the dropdown selection change to Departure Date
        with allure.step("Change dropdown option selection to 'Departure Date'"):
            partner_page.select_sort_by_departure_date()

        # 3. Grab the new top cruise card title text (Sorted by Departure Date)
        with allure.step("Capture the new top cruise title after sorting"):
            sorted_title = partner_page.get_top_cruise_title()

        # 4. Assert that the listings swapped positions successfully
        with allure.step("Asserting that the top cruise item changed"):
            print(f"[DEBUG] Comparing titles -\n Old: '{baseline_title}'\n New: '{sorted_title}'")
            
            # 🔍 THE ASSERTION: They must be different if sorting successfully executed!
            assert baseline_title != sorted_title, (
                f"❌ SORT CRITERIA ERROR: The top item did not change! "
                f"Both before and after show: '{baseline_title}'"
            )
            
            allure.attach(driver.get_screenshot_as_png(), name="Sorted Grid State Proof", attachment_type=allure.attachment_type.PNG)
            print("[SUCCESS] Test passed. Sorting modified the page grid layout successfully.")