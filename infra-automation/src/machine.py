from pydantic import BaseModel, field_validator
from typing import Dict, Any
import json, logging, subprocess

class Machine(BaseModel):
    """Represents a virtual machine with its configuration."""
    name: str
    operatingsys: str
    cpu: int
    ram: int
    disk: int

    @field_validator("name", mode = "before")
    def validate_name(cls, value: Any) -> str:
        """Validates the machine name is between 1 and 30 characters.
        
        Args:
            value: The name value to validate
            
        Returns:
            str: The validated name
            
        Raises:
            ValueError: If name is empty or longer than 30 characters
        """
        if len(value) == 0:
            raise ValueError (f"You have not entered a name.")
        if len(value) > 30:
            raise ValueError (f"The name of the machine is too long (maximum length is 30 characters). This is what you have entered: {value}")
        return value
    @field_validator("operatingsys", mode = "before")
    def validate_os(cls, value: Any) -> str:
        value = value.lower()
        allowedos = ["windows", "ubuntu", "centos", "linux", "macos", "debian", "redhat"]
        if value not in allowedos:
            raise ValueError (f"The OS you want does not exist in {allowedos}. This is what you have entered {value}")
        return value
    @field_validator("cpu", mode = "before")
    def validate_cpu(cls, value: Any) -> int:
        if value <= 0 or value > 96:
            raise ValueError (f"The cpu power you asked for is too big and it does not exist or you have entered a value that is below 0. This is what you have entered: {value}")
        return value
    @field_validator("ram", mode = "before")
    def validate_ram(cls, value: Any) -> int:
        if value <= 0 or value > 6000:
            raise ValueError (f"The ram size you asked for is too big and it does not exist or you have entered a value that is below 0. This is what you have entered: {value}")
        return value
    @field_validator("disk", mode = "before")
    def validate_disk(cls, value: Any) -> int:
        if value <= 0 or value > 3000:
            raise ValueError (f"The disk space you asked for is too big and it does not exist or you have entered a value that is below 0. This is what you have entered:  {value}")
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the machine object to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary containing machine properties
        """
        return {
            "name": self.name,
            "operatingsys": self.operatingsys,
            "cpu": self.cpu,
            "ram": self.ram,
            "disk": self.disk
            }
    
    def install_nginx(self) -> subprocess.CompletedProcess[str]:
        """Installs Nginx on the machine using a bash script.
        
        Returns:
            subprocess.CompletedProcess[str]: The result of the subprocess execution
            
        Raises:
            FileNotFoundError: If the script file is not found
            PermissionError: If execution permission is denied
            subprocess.CalledProcessError: If the script fails
        """
        pathtoscript = "infra-automation/scripts/installnginx.bash"
        result = subprocess.run(["sudo", "bash", pathtoscript], text=True, check=True)
        return result