import configparser
import os

class ConfigReader:
    @staticmethod
    def get_property(section, option):
        """
        Reads values from config.properties dynamically from the 'config' folder.
        """
        config = configparser.RawConfigParser()
        
        # Strategy A: Relative calculation assuming config reader is inside utils/ and config is a sibling folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path_a = os.path.abspath(os.path.join(current_dir, '..', 'config', 'config.properties'))
        
        # Strategy B: Fallback assuming execution starts from project root and config folder is present
        config_path_b = os.path.abspath(os.path.join(os.getcwd(), 'config', 'config.properties'))
        
        # Select the valid path location
        if os.path.exists(config_path_a):
            target_path = config_path_a
        elif os.path.exists(config_path_b):
            target_path = config_path_b
        else:
            raise FileNotFoundError(
                f"\n❌ CRITICAL PATH CONFIGURATION FAILURE:\n"
                f"The 'config.properties' file was not found inside your 'config' directory!\n"
                f"We scanned the following absolute locations:\n"
                f" 1. {config_path_a}\n"
                f" 2. {config_path_b}\n"
                f"Please verify that the folder is named 'config' and the file is named 'config.properties'."
            )
            
        config.read(target_path)
        
        try:
            return config.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError) as e:
            raise KeyError(f"❌ CONFIG ERROR: Missing section '{section}' or key '{option}' in {target_path}") from e