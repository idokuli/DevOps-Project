import json
import logging
from typing import List
from machine import Machine

class ConfigManager:
    """Manages saving and loading machine configurations to/from JSON files."""
    
    def __init__(self, config_path: str = "infra-automation/configs/instances.json") -> None:
        """Initializes ConfigManager with a configuration file path.
        
        Args:
            config_path: Path to the JSON configuration file
        """
        self.config_path = config_path
    
    def save_machines(self, machines: List[Machine]) -> bool:
        """Saves machine configurations to a JSON file.
        
        Args:
            machines: List of Machine objects to save
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        if not machines:
            logging.warning("No machines were created. JSON file will not be created.")
            return False
        
        try:
            with open(self.config_path, "w") as jsonfile:
                machines_data = [machine.to_dict() for machine in machines]
                json.dump(machines_data, jsonfile, indent=4)
                logging.info(f"All {len(machines)} machine configuration(s) have been saved in a JSON file at {self.config_path}")
                return True
        except Exception as error:
            logging.error(f"Error saving machines to JSON file: {error}")
            return False
    
    def load_machines(self) -> List[dict]:
        """Loads machine configurations from a JSON file.
        
        Returns:
            List[dict]: List of machine dictionaries, or empty list if file doesn't exist or has errors
        """
        try:
            with open(self.config_path, "r") as jsonfile:
                machines_data = json.load(jsonfile)
                logging.info(f"Loaded {len(machines_data)} machine configuration(s) from {self.config_path}")
                return machines_data
        except FileNotFoundError:
            logging.warning(f"Configuration file not found at {self.config_path}")
            return []
        except json.JSONDecodeError as error:
            logging.error(f"Error decoding JSON file: {error}")
            return []
        except Exception as error:
            logging.error(f"Error loading machines from JSON file: {error}")
            return []

