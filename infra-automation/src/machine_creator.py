import logging
from typing import List, Optional, Tuple
from pydantic import ValidationError
from machine import Machine

class MachineCreator:
    """Creates and manages Machine objects through user interaction."""
    
    def __init__(self) -> None:
        """Initializes the MachineCreator with an empty list of machines."""
        self.machines: List[Machine] = []
    
    def collect_machine_input(self) -> Optional[Tuple[str, str, int, int, int]]:
        """Collects machine configuration from user input.
        
        Returns:
            Optional[Tuple[str, str, int, int, int]]: A tuple containing (name, os, cpu, ram, disk)
            or None if input validation fails
        """
        try:
            machinename = input("What is the machine's name? ")
            operatinsys = input("What is the operating system that your server need? (windows, ubuntu, centos, linux, macos, debian, redhat) ").lower()
            cpu = int(input("How many cpu cores does your server need? "))
            ram = int(input("How many ram memory (in gigabytes) does your server need? "))
            diskspace = int(input("What is the disk space that you need? (in gigabytes) "))
            return (machinename, operatinsys, cpu, ram, diskspace)
        except ValueError as error:
            print(f"Invalid input type, error raised: {error}")
            logging.info("The user provided an invalid input type")
            return None
    
    def create_machine(self, machinename: str, operatingsys: str, cpu: int, ram: int, disk: int) -> bool:
        """Creates a Machine object and adds it to the machines list.
        
        Args:
            machinename: Name of the machine (1-30 characters)
            operatingsys: Operating system (windows, ubuntu, centos, linux, macos, debian, redhat)
            cpu: Number of CPU cores (1-96)
            ram: RAM size in GB (1-6000)
            disk: Disk space in GB (1-3000)
            
        Returns:
            bool: True if machine was created successfully, False otherwise
        """
        try:
            machine = Machine(name=machinename, operatingsys=operatingsys, cpu=cpu, ram=ram, disk=disk)
            self.machines.append(machine)
            logging.info(f"""The object has been created successfuly its properties are: Name: {machinename}, Operating System: {operatingsys}
                        CPU cores: {cpu}, RAM size: {ram} disk size: {disk}""")
            return True
        except ValidationError as error:
            print(f"Validation error: {error}")
            logging.info(f"The operation was not successfull because there is a problem with the object with the name {machinename}")
            return False
        except ValueError as error:
            print(f"Invalid input type, error raised: {error}")
            logging.info("The user provided an invalid input type")
            return False
        except NameError as error:
            print(f"Name error raised: {error}")
            logging.info("There is a name error in the code")
            return False
    
    def should_continue(self, machine_created: bool) -> bool:
        """Asks user if they want to create another machine.
        
        Args:
            machine_created: Whether the previous machine was successfully created
            
        Returns:
            bool: True if user wants to continue, False otherwise
        """
        if machine_created:
            newmach = input("Do you want to create another machine? (yes or no) ")
        else:
            newmach = input("Do you want to try creating another machine? (yes or no) ")
        
        if newmach.lower() in ["no", "false","n","f"]:
            return False
        return True
    
    def create_machines_interactive(self) -> None:
        """Interactive loop to create multiple machines until user stops.
        
        Continuously prompts the user for machine details and creates Machine objects
        until the user indicates they don't want to create more machines.
        """
        while True:
            user_input = self.collect_machine_input()
            
            if user_input is None:
                if not self.should_continue(False):
                    break
                continue
            
            machinename, operatingsys, cpu, ram, diskspace = user_input
            machine_created = self.create_machine(machinename, operatingsys, cpu, ram, diskspace)
            
            if not self.should_continue(machine_created):
                break
    
    def get_machines(self) -> List[Machine]:
        """Returns the list of created machines.
        
        Returns:
            List[Machine]: List of all Machine objects created by this MachineCreator
        """
        return self.machines

