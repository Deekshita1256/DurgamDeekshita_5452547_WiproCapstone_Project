# import pytest
# import allure
# import time
# import os

# # IMPORT SELENIUMBASE
# from seleniumbase import Driver

# from utils.logger import LogGen
# from utils.screenshot_util import ScreenshotUtil
# from utils.config_reader import ConfigReader  # Import your config reader

# logger = LogGen.loggen()


# @pytest.fixture()
# def driver():
#     logger.info("========== STARTING TEST ==========")

#     # 1. READ VALUES FROM CONFIG.PROPERTIES
#     browser_name = ConfigReader.get_property('BROWSER', 'BROWSER_NAME').lower()
#     headless_mode = ConfigReader.get_property('BROWSER', 'HEADLESS').lower() == 'true'
#     base_url = ConfigReader.get_property('ENV', 'BASE_URL')
#     imp_wait = int(ConfigReader.get_property('ENV', 'IMPLICIT_WAIT'))

#     logger.info(f"LAUNCHING BROWSER: {browser_name.upper()} (Headless={headless_mode})")

#     # 2. CREATE DRIVER USING CONFIG VALUES
#     # SeleniumBase UC mode supports browser options dynamically
#     driver = Driver(browser=browser_name, uc=True, headless=headless_mode)
#     driver.maximize_window()

#     # 3. APPLY CONFIG TIMEOUTS
#     driver.implicitly_wait(imp_wait)

#     # 4. OPEN WEBSITE FROM CONFIG
#     logger.info(f"OPENING WEBSITE: {base_url}")
#     driver.get(base_url)

#     # CRITICAL WAF WAIT: Let invisible security scripts resolve
#     time.sleep(2)

#     logger.info(f"CURRENT URL: {driver.current_url}")

#     yield driver

#     logger.info("========== CLOSING TEST ==========")
#     try:
#         driver.quit()
#         logger.info("BROWSER CLOSED SUCCESSFULLY")
#     except Exception as e:
#         logger.error(f"ERROR CLOSING BROWSER: {str(e)}")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == "call":
#         if "driver" not in item.funcargs:
#             return

#         driver = item.funcargs["driver"]

#         try:
#             if report.passed:
#                 logger.info("TEST PASSED - CAPTURING SCREENSHOT")
#                 path = ScreenshotUtil.capture(driver, f"{item.name}_PASS")  # Note: Uses fixed 'capture' name
#             else:
#                 logger.error("TEST FAILED - CAPTURING SCREENSHOT")
#                 path = ScreenshotUtil.capture(driver, f"{item.name}_FAIL")  # Note: Uses fixed 'capture' name

#             allure.attach.file(
#                 path,
#                 name="Screenshot",
#                 attachment_type=allure.attachment_type.PNG
#             )
#         except Exception as e:
#             logger.error(f"SCREENSHOT FAILED: {str(e)}")


# # AUTO OPEN ALLURE REPORT
# def pytest_unconfigure(config):
#     print("\n======= TESTS COMPLETED - OPENING ALLURE REPORT =======")
#     if not os.path.exists("reports/allure-results"):
#         os.makedirs("reports/allure-results")
#     os.system("allure serve reports/allure-results")

import pytest
import allure
import time
import os

# IMPORT SELENIUMBASE
from seleniumbase import Driver

from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil
from utils.config_reader import ConfigReader  # Import your config reader

logger = LogGen.loggen()


@pytest.fixture()
def driver():
    logger.info("========== STARTING TEST ==========")

    # 1. READ VALUES FROM CONFIG.PROPERTIES
    browser_name = ConfigReader.get_property('BROWSER', 'BROWSER_NAME').lower()
    headless_mode = ConfigReader.get_property('BROWSER', 'HEADLESS').lower() == 'true'
    base_url = ConfigReader.get_property('ENV', 'BASE_URL')
    imp_wait = int(ConfigReader.get_property('ENV', 'IMPLICIT_WAIT'))

    logger.info(f"LAUNCHING BROWSER: {browser_name.upper()} (Headless={headless_mode})")

    # 2. CREATE DRIVER USING CONFIG VALUES
    # SeleniumBase UC mode supports browser options dynamically
    driver = Driver(browser=browser_name, uc=True, headless=headless_mode)
    driver.maximize_window()

    # 3. APPLY CONFIG TIMEOUTS
    driver.implicitly_wait(imp_wait)

    # 4. OPEN WEBSITE FROM CONFIG
    logger.info(f"OPENING WEBSITE: {base_url}")
    driver.get(base_url)

    # CRITICAL WAF WAIT: Let invisible security scripts resolve
    time.sleep(2)

    logger.info(f"CURRENT URL: {driver.current_url}")

    yield driver

    logger.info("========== CLOSING TEST ==========")
    try:
        driver.quit()
        logger.info("BROWSER CLOSED SUCCESSFULLY")
    except Exception as e:
        logger.error(f"ERROR CLOSING BROWSER: {str(e)}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if "driver" not in item.funcargs:
            return

        driver = item.funcargs["driver"]

        try:
            if report.passed:
                logger.info("TEST PASSED - CAPTURING SCREENSHOT")
                path = ScreenshotUtil.capture(driver, f"{item.name}_PASS")  # Note: Uses fixed 'capture' name
            else:
                logger.error("TEST FAILED - CAPTURING SCREENSHOT")
                path = ScreenshotUtil.capture(driver, f"{item.name}_FAIL")  # Note: Uses fixed 'capture' name

            allure.attach.file(
                path,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            logger.error(f"SCREENSHOT FAILED: {str(e)}")


# AUTO GENERATE AND OPEN ALLURE REPORT
def pytest_unconfigure(config):
    print("\n======= TESTS COMPLETED - GENERATING ALLURE REPORT =======")
    
    # Ensure the results directory exists to avoid generation errors
    if not os.path.exists("reports/allure-results"):
        os.makedirs("reports/allure-results")
        
    # Compile JSON results into static HTML in the reports/allure-report directory
    os.system("allure generate reports/allure-results -o reports/allure-report --clean")
    
    # Open the generated HTML report
    os.system("allure open reports/allure-report")