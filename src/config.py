"""
Configuration management for the application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    # Application Settings
    APP_TITLE = os.getenv("APP_TITLE", "GenAI Live Environment Assistant")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DUMMY_DATA_DIR = os.path.join(BASE_DIR, "dummy_data")
    LOGS_DIR = os.path.join(DUMMY_DATA_DIR, "logs")
    METRICS_DIR = os.path.join(DUMMY_DATA_DIR, "metrics")
    CODEBASE_DIR = os.path.join(DUMMY_DATA_DIR, "codebase")
    
    # LangChain Settings
    MAX_TOKENS = 4096
    TEMPERATURE = 0.2  # Lower temperature for more consistent analysis
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.AZURE_OPENAI_API_KEY:
            raise ValueError("AZURE_OPENAI_API_KEY not set in environment variables")
        if not cls.AZURE_OPENAI_ENDPOINT:
            raise ValueError("AZURE_OPENAI_ENDPOINT not set in environment variables")
        if not cls.AZURE_OPENAI_DEPLOYMENT_NAME:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME not set in environment variables")
        return True
