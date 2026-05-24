import os
import sys
import allure
import time
import logging
from seleniumbase import Driver
from utils.config_reader import ConfigReader
from utils.logger import LogGen
from allure_commons.types import AttachmentType

# Initialize your custom logger utility
logger = LogGen.loggen()

def before_all(context):
    """Executes once before the entire test suite starts."""
    logger.info("========== BDD TEST SUITE INITIALIZATION ==========")
    
    # Ensure local directory paths for allure results exist
    if not os.path.exists("reports/allure-results"):
        os.makedirs("reports/allure-results")

def before_scenario(context, scenario):
    """Executes before every individual scenario loop."""
    logger.info(f"--> STARTING SCENARIO: {scenario.name}")
    
    # 1. Read values from config.properties
    browser_name = ConfigReader.get_property('BROWSER', 'BROWSER_NAME').lower()
    headless_mode = ConfigReader.get_property('BROWSER', 'HEADLESS').lower() == 'true'
    base_url = ConfigReader.get_property('ENV', 'BASE_URL')
    imp_wait = int(ConfigReader.get_property('ENV', 'IMPLICIT_WAIT'))

    logger.info(f"LAUNCHING BROWSER: {browser_name.upper()} (Headless={headless_mode})")

    # 2. Spin up Driver instance via SeleniumBase UC Mode
    context.driver = Driver(browser=browser_name, uc=True, headless=headless_mode)
    context.driver.maximize_window()
    context.driver.implicitly_wait(imp_wait)

    # 🌟 INSTANTIATE ALL PAGE OBJECTS GLOBALLY HERE:
    from pages.cruise_page import CruisePage
    from pages.partner_cruise_page import PartnerCruisePage
    from pages.cabin_selection_page import CabinSelectionPage
    from pages.passenger_details_page import PassengerDetailsPage
    from pages.payment_page import PaymentPage

    context.cruise_page = CruisePage(context.driver)
    context.partner_page = PartnerCruisePage(context.driver)
    context.cabin_page = CabinSelectionPage(context.driver)
    context.passenger_page = PassengerDetailsPage(context.driver)
    context.payment_page = PaymentPage(context.driver)

    # 3. Direct browser to baseline endpoint target
    logger.info(f"OPENING WEBSITE: {base_url}")
    context.driver.get(base_url)

def after_scenario(context, scenario):
    """Executes immediately after a scenario finishes (handles Screenshots and Logs)."""
    logger.info(f"<-- ENDING SCENARIO: {scenario.name} | STATUS: {scenario.status}")

    if hasattr(context, "driver"):
        # 📸 SCENARIO LEVEL BACKUP IN CASE OF CRITICAL BREAKAGE
        if scenario.status == "failed":
            logger.error(f"TEST FAILED: '{scenario.name}' - CAPTURING FINAL TRACE")

        # 🛑 CLEAN UP AND BROWSER TEARDOWN
        try:
            context.driver.quit()
            logger.info("BROWSER CLOSED SUCCESSFULLY")
        except Exception as e:
            logger.error(f"Error during browser teardown context exit: {str(e)}")

# 🌟 ADDED: AFTER STEP HOOK FOR CHRONOLOGICAL SNAPSHOTS ───────────────────
def after_step(context, step):
    """Executes automatically right after every individual step completes (Passed & Failed)."""
    if not hasattr(context, "driver"):
        return

    # 1. Base reports folder path setup
    base_dir = os.path.join(os.getcwd(), "reports", "screenshots")
    
    # 2. Separate subdirectory structures based on step validation outcome
    if step.status == "passed":
        screenshot_dir = os.path.join(base_dir, "passed")
        prefix = "PASSED"
    elif step.status == "failed":
        screenshot_dir = os.path.join(base_dir, "failed")
        prefix = "FAILED"
        logger.error(f"❌ Step Failed: '{step.name}' - Capturing viewpoint snapshot.")
    else:
        return  # Ignore skipped or undefined steps

    # 3. Guard: Ensure the directory paths exist on disk
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # 4. Create a clean filename from the Gherkin step text
    clean_step_name = step.name.replace(" ", "_").replace('"', "").replace(":", "")
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    screenshot_name = f"{prefix}_{clean_step_name}_{timestamp}.png"
    screenshot_path = os.path.join(screenshot_dir, screenshot_name)

    try:
        # 5. Capture the physical file on disk for local storage inspection
        context.driver.save_screenshot(screenshot_path)
        
        # 6. Embed the image directly into your interactive Allure report node tree
        allure.attach(
            context.driver.get_screenshot_as_png(),
            name=f"{prefix}: {step.name}",
            attachment_type=AttachmentType.PNG
        )
    except Exception as e:
        logger.error(f"⚠️ Warning: Could not capture step screenshot: {str(e)}")

# ──────────────────────────────────────────────────────────────────────────

def after_all(context):
    """Executes once after all features and scenarios complete execution."""
    print("\n======= BDD TESTS COMPLETED - COMPILING ALLURE REPORT =======")
    logger.info("========== BDD TEST SUITE COMPLETION - COMPILING REPORT ==========")
    
    # Automatically host and pop open your Allure Report instantly via system call
    os.system("allure serve reports/allure-results")