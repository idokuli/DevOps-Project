import logging
import subprocess
from typing import List
from machine import Machine

class ServiceInstaller:
    """Handles installation of services (like Nginx) on machines."""
    
    def install_nginx(self, machine: Machine) -> bool:
        """Installs Nginx on a single machine.
        
        Args:
            machine: The Machine object to install Nginx on
            
        Returns:
            bool: True if installation succeeded, False otherwise
        """
        try:
            logging.info(f"Installing Nginx for machine: {machine.name}")
            machine.install_nginx()
            print(f"Nginx installation completed successfully for {machine.name}")
            logging.info(f"Nginx installation completed successfully for machine: {machine.name}")
            return True
        except FileNotFoundError as error:
            print(f"File or Directory not found, error raised: {error}")
            logging.info(f"File or Directory for Linux script not found for machine: {machine.name}")
            return False
        except PermissionError as error:
            print(f"Permission denied: {error}")
            logging.info(f"The requested file does not have the right permission to execute the script for machine: {machine.name}")
            return False
        except subprocess.CalledProcessError as error:
            print(f"The command failed with exit code: {error.returncode}")
            logging.info(f"Something went wrong with the script for machine {machine.name}, because it exited with a wrong exit code")
            return False
        except Exception as error:
            print(f"Unexpected error during Nginx installation: {error}")
            logging.error(f"Unexpected error installing Nginx for machine {machine.name}: {error}")
            return False
    
    def install_nginx_for_all(self, machines: List[Machine]) -> None:
        """Installs Nginx on all machines in the provided list.
        
        Args:
            machines: List of Machine objects to install Nginx on
        """
        if not machines:
            logging.warning("No machines provided for service installation")
            return
        
        logging.info(f"Starting service installation for {len(machines)} machine(s)")
        for machine in machines:
            self.install_nginx(machine)

