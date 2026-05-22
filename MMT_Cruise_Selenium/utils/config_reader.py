import configparser
import os

class ConfigReader:

    @staticmethod
    def get_property(section, key):
        config = configparser.ConfigParser()
        
        # Absolute path strategy: locate where this file sits, then move cleanly across folders
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        config_path = os.path.join(project_root, "config", "config.properties")

        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file missing at discovered path: {config_path}")

        # This reads the exact properties file
        config.read(config_path, encoding='utf-8')
        
        if not config.has_section(section):
            raise configparser.NoSectionError(f"Section '{section}' missing from configuration file layout at: {config_path}")
            
        return config.get(section, key)