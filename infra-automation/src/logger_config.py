import logging

class LoggerConfig:
    """Configuration and utilities for logging infrastructure provisioning activities"""
    @staticmethod
    def setup_logging(log_file: str = "infra-automation/logs/provisioning.log", level: int = logging.INFO):
        """Configures the logging system with file handler

        Args:
            log_file: Path to log file
            level: Logging level (default: logging.INFO)
        """
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file)
            ]
        )
    
    @staticmethod
    def log_provisioning_start():
        print("=== Infrastructure provisioning started ===")
        logging.info("=== Infrastructure provisioning started ===")
    
    @staticmethod
    def log_provisioning_end():
        logging.info("=== Infrastructure provisioning completed ===")
        print("=== Infrastructure provisioning completed ===")

