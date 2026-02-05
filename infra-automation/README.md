# Infra-Automation Technical Details

This directory contains the Python core and Terraform modules for the infrastructure automation suite.

## 🐍 Python Components (`src/`)

### `infra_simulator.py`
The main entry point. It orchestrates the entire flow:
*   Collects machine data via `MachineCreator`.
*   Groups machines by region to support multi-region "waves".
*   Triggers Terraform runs with isolated state files (`-state=terraform.region.tfstate`).

### `machine.py`
The data model. Powered by **Pydantic**, it validates all inputs and automatically "cleans" user typos (like stripping brackets or quotes from AMI IDs).

### `machine_creator.py`
Handles the interactive CLI loop for adding machines.

---

## 🏗️ Terraform Modules (`Terraform/`)

### `Deployments/`
The root module. It handles the `instances` map and calls the child modules using `for_each`.

### `Custom_vpc_ec2/`
Provisioning logic for networking and the core server. Includes automatic SSH key generation.

### `LB_TG_AS/`
Provisioning logic for the Load Balancer, Target Groups, and Auto Scaling Group.

---

## 🔐 Security Note
All private keys (`.pem`) and state files (`.tfstate`) are automatically ignored by Git (see root `.gitignore`). **Never commit these files to a public repository.**