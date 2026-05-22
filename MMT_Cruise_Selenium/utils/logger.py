import logging
import os


class LogGen:
    @staticmethod
    def loggen():
        # Ensure log directory path is resolved correctly relative to project root
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_file_path = os.path.join(log_dir, 'automation.log')

        # Reset handlers to avoid duplicated log prints across multiple test iterations
        logger = logging.getLogger()
        if logger.hasHandlers():
            logger.handlers.clear()

        # Define structured readable format
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # 1. File Handler (Writes to logs/automation.log)
        file_handler = logging.FileHandler(filename=log_file_path, mode='a', encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # 2. Stream Handler (Outputs to terminal/PyCharm console)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.setLevel(logging.INFO)
        return logger


# Globally accessible logger instance for simple importing
logger = LogGen.loggen()