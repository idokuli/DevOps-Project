from pydantic import BaseModel, field_validator, ValidationInfo
from typing import Dict, Any
import json, logging, subprocess

class Machine(BaseModel):
    """Represents a virtual machine with its configuration."""
    region: str
    name: str
    ami_id: str
    instance_type: str

    @field_validator("region", mode = "before")
    def validate_region(cls, value: Any) -> str:
        value = value.lower()
        allowed_regions = ["us-east-1", "eu-west-1", "ap-south-1", "us-west-2", "eu-west-2", "ap-southeast-2", "us-east-2", "eu-central-1", "ap-northeast-1", "ap-northeast-2", "ap-southeast-1", "ca-central-1", "sa-east-1", "us-west-1", "eu-north-1"]
        if value not in allowed_regions:
            raise ValueError (f"The region you want does not exist in {allowed_regions}. This is what you have entered {value}")
        return value
    @field_validator("name", mode = "before")
    def validate_name(cls, value: Any) -> str:
        if len(value) == 0:
            raise ValueError (f"You have not entered a name.")
        if len(value) > 30:
            raise ValueError (f"The name of the machine is too long (maximum length is 30 characters). This is what you have entered: {value}")
        return value
    
    @field_validator("ami_id", mode = "before")
    def validate_ami_id(cls, value: Any) -> str:
        import re
        if not re.match(r"^ami-[0-9a-f]{8,17}$", value):
            raise ValueError("Format must be 'ami-' followed by hex characters.")
        return value
    @field_validator("instance_type", mode = "before")
    def validate_instance_type(cls, value: Any, info: ValidationInfo) -> str:
        forbidden_keywords = ["metal", "16xlarge", "32xlarge", "96xlarge"]
        if any(size in value for size in forbidden_keywords):
            raise ValueError(f"Instance type '{value}' is too expensive for this project.")
        allowed_families = ('t', 'm')
        if not value.startswith(allowed_families):
            raise ValueError("Only 'T' (Burstable) or 'M' (General Purpose) instances are permitted.")
        region = info.data.get("region")
        if region == "us-east-1" and "xlarge" in value:
            raise ValueError(f"xlarge instances are not permitted in {region} due to quota limits.")
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        """Converts the machine object to a dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary containing machine properties
        """
        return {
            "name": self.name,
            "region": self.region,
            "ami_id": self.ami_id,
            "instance_type": self.instance_type
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