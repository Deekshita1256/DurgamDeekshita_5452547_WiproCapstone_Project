import logging
import os

class LogGen:
    @staticmethod
    def loggen():
        """
        Generates and configures a centralized logger instance.
        Usage: 
            from utils.logger import LogGen
            logger = LogGen.loggen()
            logger.info("Message here")
        """
        # Ensure the logs/ tracking directory exists in the root folder
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        log_filepath = os.path.join(log_dir, "automation.log")

        # Create a logger instance
        logger = logging.getLogger("MMT_Cruise_Automation")
        
        # If the logger has handlers already, don't re-add them (prevents duplicate logs)
        if not logger.handlers:
            logger.setLevel(logging.INFO)

            # Define a crisp, clean layout format for timestamped logs
            formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # 1. File Handler: Writes out detailed tracking info to automation.log
            file_handler = logging.FileHandler(log_filepath, mode="a", encoding="utf-8")
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.INFO)
            logger.addHandler(file_handler)

            # 2. Console Handler: Dumps tracking info live to your running terminal workspace
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)
            logger.addHandler(console_handler)

        return logger