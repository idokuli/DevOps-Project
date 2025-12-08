# DevOps Infrastructure Provisioning & Configuration Automation Project

## Overview

This Python-based tool simulates provisioning virtual machines and automating service setup using Bash scripts. It accepts user input for VM definitions, validates them using Pydantic, and follows a clean, modular class-based architecture with comprehensive logging and robust error handling.
While the current implementation mocks infrastructure behavior, future updates will integrate AWS and Terraform for real-world cloud provisioning.

## Architecture

The project follows a modular, object-oriented design with clear separation of concerns:

- **`LoggerConfig`**: Handles logging configuration and setup
- **`MachineCreator`**: Manages user input collection and Machine object creation
- **`ConfigManager`**: Handles saving and loading machine configurations to/from JSON files
- **`ServiceInstaller`**: Manages service installation (e.g., Nginx) on machines
- **`Machine`**: Pydantic model representing a virtual machine with validation
- **`infra_simulator.py`**: Main entry point that orchestrates the provisioning workflow

### Prerequisites
- Python 3.7+
- Linux/Unix system
- sudo privileges

### Setup

   **Run the automation program**

   **IMPORTANT**: You must run all commands from the project root folder (`DevOps-Project/`)

   Running the code from anywhere else will cause Python and the Bash scripts to fail due to relative path dependencies.

    ```bash
    # 1. Navigate to project root
    cd DevOps-Project

    # 2. Create virtual environment
    python3 -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate

    # 3. Install dependencies
    pip install -r infra-automation/requirements.txt

    # 4. Run the program (MUST be from project root!)
    python infra-automation/src/infra_simulator.py
    ```

## Usage

The program will prompt you for:
- **Machine name** (1-30 characters)
- **Operating system** (`windows`, `ubuntu`, `centos`, `linux` `macos`, `debian`, `redhat`)
- **CPU cores** (1-96)
- **RAM** (1-6000 GB)
- **Disk space** (1-3000 GB)

After each machine, choose to create another or finish.

## What It Does

The program follows this workflow:

1. ✅ **Logging Setup**: Configures logging system via `LoggerConfig`
2. ✅ **Machine Creation**: Collects user input and creates validated `Machine` objects via `MachineCreator`
3. ✅ **Configuration Management**: Saves all machine configurations to JSON via `ConfigManager`
4. ✅ **Service Installation**: Installs Nginx on all machines via `ServiceInstaller`
5. ✅ **Comprehensive Logging**: All operations are logged to `infra-automation/logs/provisioning.log`

## Project Structure

```
DevOps-Project/
 ├── infra-automation/
 │    ├── configs/          # instances.json (output)
 │    ├── logs/             # provisioning.log
 │    ├── scripts/          # installnginx.bash
 │    └── src/
 │         ├── Machine.py              # Machine class (Pydantic model)
 │         ├── LoggerConfig.py         # Logging configuration class
 │         ├── MachineCreator.py       # Machine creation and user input handling
 │         ├── ConfigManager.py        # JSON configuration file management
 │         ├── ServiceInstaller.py     # Service installation management
 │         └── infra_simulator.py      # Main entry point
 └── requirements.txt
```

## Class Responsibilities

### LoggerConfig
- Configures Python logging system
- Provides static methods for logging start/end of provisioning
- Manages log file output

### MachineCreator
- Collects machine configuration from user input
- Validates and creates `Machine` objects
- Manages interactive loop for creating multiple machines
- Handles input validation errors gracefully

### ConfigManager
- Saves machine configurations to JSON files
- Loads machine configurations from JSON files
- Handles file I/O errors and validation

### ServiceInstaller
- Installs services (e.g., Nginx) on machines
- Handles installation errors (file not found, permissions, etc.)
- Supports batch installation for multiple machines

### Machine
- Pydantic model with validation for:
  - Name (1-30 characters)
  - Operating system (validated against allowed list)
  - CPU cores (1-96)
  - RAM (1-6000 GB)
  - Disk space (1-3000 GB)
- Provides methods for dictionary conversion and service installation

## Troubleshooting

**Error: File not found**
- Make sure you're running from `DevOps-Project/` root directory

**Error: Permission denied**
- Ensure you have sudo privileges for Nginx installation

**Validation errors**
- Check that your inputs match the validation rules above

## Future Enhancements

- AWS integration for real instance provisioning
- Terraform automation
- Additional services and configurations