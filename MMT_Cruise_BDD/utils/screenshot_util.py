import os
import time
from utils.logger import LogGen

# Initialize your custom logger utility
logger = LogGen.loggen()

class ScreenshotUtil:
    @staticmethod
    def capture(driver, name_suffix):
        """
        Captures a high-resolution screenshot of the current viewport,
        saves it physically under the screenshots/ directory, and returns the path.
        
        Usage:
            path = ScreenshotUtil.capture(driver, "PASS_CRUISE_SEARCH")
        """
        try:
            # Step 1: Define and ensure the local screenshots storage folder exists
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            screenshot_dir = os.path.join(project_root, "screenshots")
            
            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)

            # Step 2: Build a unique timestamped filename to prevent overwrites
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_name = f"{name_suffix}_{timestamp}.png"
            full_filepath = os.path.join(screenshot_dir, file_name)

            # Step 3: Take and save the viewport file via Selenium
            driver.save_screenshot(full_filepath)
            
            logger.info(f"📸 SCREENSHOT CAPTURED SUCCESSFULLY: {full_filepath}")
            return full_filepath

        except Exception as e:
            logger.error(f"❌ SCREENSHOT UTILITY TRACKING FAILURE: {str(e)}")
            return ""