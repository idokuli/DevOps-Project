# DevOps Infrastructure Provisioning & Configuration Automation Project

## Overview

This tool automates the provisioning of high-availability AWS infrastructure. It orchestrates **completely isolated stacks** (dedicated VPC and Load Balancer per machine) across multiple AWS regions using an intelligent Python wrapper around Terraform. 

The system uses **Pydantic** for robust configuration validation and automatically "cleans" user inputs (stripping typos like brackets or quotes) before triggering Terraform waves.

## Architecture

The project follows a modular, object-oriented design with clear separation of concerns:

- **`LoggerConfig`**: Handles logging configuration and multi-region session logging.
- **`MachineCreator`**: Manages interactive user input collection and Machine object creation.
- **`ConfigManager`**: Handles saving and loading machine configurations to/from JSON files (the bridge to Terraform).
- **`Machine`**: Pydantic model representing a virtual machine with validation and automated input cleaning.
- **`infra_simulator.py`**: The main orchestrator that groups machines by region and executes isolated Terraform "waves."

### Prerequisites
- Python 3.10+
- [Terraform](https://www.terraform.io/downloads) installed and in PATH
- AWS CLI configured (`aws configure`)
- Valid AWS credentials

### Setup

**IMPORTANT**: You must run all commands from the project root folder (`DevOps-Project/`).

```bash
# 1. Navigate to project root
cd DevOps-Project

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r infra-automation/requirements.txt

# 4. Run the program
python infra-automation/src/infra_simulator.py
```

## Usage

The program will prompt you for:
- **Region**: (e.g., `us-east-1`, `eu-north-1`)
- **Machine name**: (1-30 characters)
- **AMI ID**: (Valid AMI for the chosen region)
- **Instance Type**: (`t` or `m` families only)

After each machine, choose to create another or finish. The script will then deploy them in regional waves.

## What It Does

The program follows this workflow:

1. ✅ **Logging Setup**: Configures the multi-region logging system.
2. ✅ **Machine Validation**: Collects input and "cleans" it (stripping `[]` or `"`) via Pydantic.
3. ✅ **Region Grouping**: Sorts machines into regional batches to prevent state conflicts.
4. ✅ **Terraform Orchestration**: Dynamically writes `tfvars` and runs `terraform apply` with isolated state files (`terraform.region.tfstate`).
5. ✅ **Service Installation**: Terraform automatically installs Nginx and Stress-ng via SSH once the server is live.

## Project Structure

```
DevOps-Project/
 ├── infra-automation/
 │    ├── Terraform/        # Modular VPC, EC2, and Load Balancer blueprints
 │    ├── configs/          # instances.json
 │    ├── logs/             # provisioning.log
 │    └── src/
 │         ├── machine.py              # Machine class (Pydantic model)
 │         ├── logger_config.py        # Logging configuration class
 │         ├── machine_creator.py      # Machine creation and input handling
 │         ├── config_manager.py       # JSON variables management
 │         └── infra_simulator.py      # Multi-region orchestrator
 ├── README.md
 ├── ARCHITECTURE.md
 └── requirements.txt
```

## Class Responsibilities

### Machine
- Validates Region and Instance types against AWS constraints.
- **Cleans Input**: Automatically detects and removes brackets `[]` or quotes from user entries.

### infra_simulator.py
- **Multi-Region Waves**: Groups machines to ensure that one Terraform provider doesn't overwrite a different region.
- **State Isolation**: Uses the `-state` flag to keep `us-east-1` resources separate from `eu-north-1`.

## Troubleshooting

**Error: InvalidAMIID.NotFound**
- Ensure your AMI ID belongs to the region you selected.
- The simulator now automatically fixes brackets like `[ami-xxxx]`, but the ID must still exist in that region.

**Error: DuplicateProvider**
- This occurs if different regions are mixed in a way that Terraform cannot resolve. The simulator now handles this via regional waves.

**Manual Cleanup**
- To destroy resources, you must specify the regional state file:
  `terraform -chdir=... destroy -state=terraform.us-east-1.tfstate`

---

## 📘 Documentation

For a deeper dive into how the system works, check out the [Architecture Overview](./ARCHITECTURE.md).