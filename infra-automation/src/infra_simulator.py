from machine_creator import MachineCreator
from config_manager import ConfigManager
from service_installer import ServiceInstaller
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
    
    config_manager = ConfigManager()
    config_manager.save_machines(machines)

    service_installer = ServiceInstaller()
    service_installer.install_nginx_for_all(machines)
    
    LoggerConfig.log_provisioning_end()


if __name__ == "__main__":
    main()
