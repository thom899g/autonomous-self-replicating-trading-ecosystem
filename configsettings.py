"""
Core configuration management for the Autonomous Self-Replicating Trading Ecosystem.
Uses Pydantic for validation and environment variable management.
"""
import os
from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

load_dotenv()

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class FirebaseConfig(BaseSettings):
    """Firebase configuration with validation"""
    project_id: str = Field(..., env="FIREBASE_PROJECT_ID")
    private_key_id: str = Field(..., env="FIREBASE_PRIVATE_KEY_ID")
    private_key: str = Field(..., env="FIREBASE_PRIVATE_KEY")
    client_email: str = Field(..., env="FIREBASE_CLIENT_EMAIL")
    client_id: str = Field(..., env="FIREBASE_CLIENT_ID")
    client_x509_cert_url: str = Field(..., env="FIREBASE_CLIENT_CERT_URL")
    
    @validator('private_key')
    def format_private_key(cls, v):
        """Format private key with proper line breaks"""
        if "\\n" in v:
            return v.replace('\\n', '\n')
        return v

class TradingConfig(BaseSettings):
    """Trading-specific configuration"""
    initial_capital: float = Field(100000.0, env="INITIAL_CAPITAL")
    max_drawdown_limit: float = Field(0.2, env="MAX_DRAWDOWN_LIMIT")
    max_position_size: float = Field(0.1, env="MAX_POSITION_SIZE")
    supported_exchanges: List[str] = Field(["binance", "coinbase", "kraken"], env="SUPPORTED_EXCHANGES")
    risk_free_rate: float = Field(0.02, env="RISK_FREE_RATE")
    
class LoggingConfig(BaseSettings):
    """Logging configuration"""
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("logs/ecosystem.log", env="LOG_FILE")
    max_file_size_mb: int = Field(100, env="MAX_LOG_SIZE_MB")
    backup_count: int = Field(5, env="LOG_BACKUP_COUNT")

class Settings(BaseSettings):
    """Main settings container with dependency injection support"""
    
    # Environment
    environment: Environment = Field(Environment.DEVELOPMENT, env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")
    
    # Component configurations
    firebase: FirebaseConfig = FirebaseConfig()
    trading: TradingConfig = TradingConfig()
    logging: LoggingConfig = LoggingConfig()
    
    # API Keys (sensitive)
    telegram_bot_token: Optional[str] = Field(None, env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(None, env="TELEGRAM_CHAT_ID")
    
    # Paths
    data_directory: str = Field("data/", env="DATA_DIRECTORY")
    strategies_directory: str = Field("strategies/", env="STRATEGIES_DIRECTORY")
    
    # Evolution Parameters
    generation_interval_minutes: int = Field(60, env="GENERATION_INTERVAL")
    evaluation_period_days: int = Field(30, env="EVALUATION_PERIOD")
    survival_rate: float = Field(0.2, env="SURVIVAL_RATE")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Validate critical paths exist
def validate_directories():
    """Ensure required directories exist"""
    directories = [
        settings.data_directory,
        settings.strategies_directory,
        "logs/",
        "backups/"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        if not os.path.exists(directory):
            raise RuntimeError(f"Failed to create directory: {directory}")

# Initialize on import
validate_directories()