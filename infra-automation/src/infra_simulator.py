import json
import subprocess
from machine_creator import MachineCreator
from config_manager import ConfigManager
from logger_config import LoggerConfig

def main():
    """Main function to orchestrate the infrastructure provisioning process.

    Sets up logging, collects machine configurations from user,
    saves configurations to JSON and installs Nginx on all machines
    """
    LoggerConfig.setup_logging()
    LoggerConfig.log_provisioning_start()
    
    machine_creator = MachineCreator()
    machine_creator.create_machines_interactive()
    machines = machine_creator.get_machines()
    
    if not machines:
        print("No machines to provision. Exiting.")
        return

    # Group machines by region for isolated Terraform runs
    region_groups = {}
    for machine in machines:
        if machine.region not in region_groups:
            region_groups[machine.region] = []
        region_groups[machine.region].append(machine)

    config_manager = ConfigManager()
    
    for region, region_machines in region_groups.items():
        print(f"\n--- Provisioning machines in region: {region} ---")
        
        # Prepare variables for this region's Terraform run
        machines_data = [m.to_dict() for m in region_machines]
        terraform_vars = {
            "instances": {m["name"]: m for m in machines_data},
            "aws_region": region
        }
        
        tfvars_path = "infra-automation/Terraform/Modules/Deployments/terraform.tfvars.json"
        with open(tfvars_path, "w") as f:
            json.dump(terraform_vars, f, indent=4)
        
        # State file path unique to this region
        state_file = f"terraform.{region}.tfstate"
        chdir_arg = "-chdir=infra-automation/Terraform/Modules/Deployments"
        
        print(f"Initializing and applying Terraform for {region}...")
        subprocess.run(["terraform", chdir_arg, "init"], check=True)
        
        # Run apply with isolated state file
        subprocess.run([
            "terraform", chdir_arg, "apply", 
            f"-state={state_file}", 
            "-auto-approve"
        ], check=True)
        
        print(f"Provisioning for {region} complete.")
    
    LoggerConfig.log_provisioning_end()


if __name__ == "__main__":
    main()