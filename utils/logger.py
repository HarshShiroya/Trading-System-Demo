import logging
import os
from datetime import datetime
from config import Config

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with file and console handlers.
    
    Args:
        name: The name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Create file handler
    log_file = os.path.join(
        Config.LOG_DIR,
        f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create main application logger
app_logger = setup_logger('techfin')

def log_exception(logger: logging.Logger, exc: Exception, context: str = None):
    """
    Log an exception with context information.
    
    Args:
        logger: The logger instance to use
        exc: The exception to log
        context: Additional context information
    """
    message = f"Exception occurred: {str(exc)}"
    if context:
        message = f"{context} - {message}"
    logger.exception(message) 