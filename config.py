import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import pandas as pd

# Load environment variables
load_dotenv()

# Configuration class for managing settings
class Config:
    # API Settings
    API_KEY = os.getenv('SMART_API_KEY', '')
    
    # Trading Settings
    SYMBOLS = ['NIFTY', 'BANKNIFTY']
    ORDER_TYPES = ['MARKET', 'LIMIT']
    OPTION_TYPES = ['CE', 'PE']
    SEGMENT_TYPES = ['OPTION', 'FUTURE']
    
    # Application Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # File paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_DIR = os.path.join(BASE_DIR, 'logs')
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    
    @staticmethod
    def setup_directories():
        """Create necessary directories if they don't exist."""
        for directory in [Config.LOG_DIR, Config.DATA_DIR]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    @staticmethod
    def get_encryption_key():
        """Get or generate encryption key for sensitive data."""
        key_file = os.path.join(Config.DATA_DIR, '.key')
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key

# Create necessary directories
Config.setup_directories()

# Create encryption instance
fernet = Fernet(Config.get_encryption_key())

def encrypt_credentials(client_code: str, password: str) -> tuple:
    """Encrypt client credentials."""
    return (
        fernet.encrypt(client_code.encode()).decode(),
        fernet.encrypt(password.encode()).decode()
    )

def decrypt_credentials(encrypted_code: str, encrypted_pass: str) -> tuple:
    """Decrypt client credentials."""
    return (
        fernet.decrypt(encrypted_code.encode()).decode(),
        fernet.decrypt(encrypted_pass.encode()).decode()
    )

# Example .env file content template
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write("""# API Configuration
SMART_API_KEY=your_api_key_here

# Application Settings
DEBUG=False
LOG_LEVEL=INFO
""") 