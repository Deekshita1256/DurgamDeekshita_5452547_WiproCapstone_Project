from behave import given
from pages.cruise_page import CruisePage

@given('the user has navigated to the Cruise module tab')
def step_impl(context):
    # context.cruise_page is already instantiated globally by environment.py option 1!
    
    # 1. Clear out the overlay modal immediately
    context.cruise_page.dismiss_login_if_present()
    
    # 2. Safely click and navigate into the main Cruise segment view
    context.cruise_page.navigate_to_cruises()