import logging
from typing import List, Optional, Tuple
from pydantic import ValidationError
from machine import Machine

class MachineCreator:
    """Creates and manages Machine objects through user interaction."""
    
    def __init__(self) -> None:
        """Initializes the MachineCreator with an empty list of machines."""
        self.machines: List[Machine] = []
    
    def collect_machine_input(self) -> Optional[Tuple[str, str, str, str]]:
        """Collects machine configuration from user input.
        
        Returns:
            Optional[Tuple[str, str, Optional[str], str]]: A tuple containing (region, name, ami_id, instance_type)
            or None if input validation fails
        """
        try:
            region = input("On which region do you want to create the machine? (e.g. us-east-1, eu-west-1, ap-south-1) ").strip()
            machinename = input("What is the machine's name? ").strip()
            ami_id = input("What is the AMI ID that your server need? (e.g. ami-01fd6fa49060e89a6) ").lower().strip()
            instance_type = input("What is the instance type that your server need? (e.g. t3.micro) ").lower().strip()
            if(instance_type == ""):
                instance_type = "t3.micro"
            return (region, machinename, ami_id, instance_type)
        except ValueError as error:
            print(f"Invalid input type, error raised: {error}")
            logging.info("The user provided an invalid input type")
            return None
    
    def create_machine(self, region: str, machinename: str, ami_id: str, instance_type: str) -> bool:
        """Creates a Machine object and adds it to the machines list.
        
        Args:
            region: Region where the machine will be created
            machinename: Name of the machine (1-30 characters)
            ami_id: AMI ID of the machine
            instance_type: Instance type of the machine
            
        Returns:
            bool: True if machine was created successfully, False otherwise
        """
        try:
            machine = Machine(region=region, name=machinename, ami_id=ami_id, instance_type=instance_type)
            self.machines.append(machine)
            logging.info(f"""The object has been created successfuly its properties are: Region: {region}, Name: {machinename}, AMI ID: {ami_id}
                        Instance Type: {instance_type}""")
            return True
        except ValidationError as error:
            # Build a detailed error message
            error_details = [f"The operation was not successful because there is a problem with the object with the name {machinename}"]
            error_details.append("Validation errors:")
            
            for err in error.errors():
                field = err['loc'][0]
                message = err['msg']
                error_details.append(f"  - {field}: {message}")
                print(f"Validation error for '{field}': {message}")
            
            # Log as multi-line message
            logging.info("\n".join(error_details))
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
            
            region, machinename, ami_id, instance_type = user_input
            machine_created = self.create_machine(region, machinename, ami_id, instance_type)
            
            if not self.should_continue(machine_created):
                break
    
    def get_machines(self) -> List[Machine]:
        """Returns the list of created machines.
        
        Returns:
            List[Machine]: List of all Machine objects created by this MachineCreator
        """
        return self.machines