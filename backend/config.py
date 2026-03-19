from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Настройки API
    API_TITLE: str = "Word Statistics API"
    API_VERSION: str = "1.0.0"
    
    # Настройки файлов
    MAX_FILE_SIZE_MB: int = 100
    ALLOWED_EXTENSIONS: set = {'.txt', '.doc', '.docx'}
    
    # Директории
    UPLOAD_DIR: str = "uploads"
    RESULTS_DIR: str = "results"
    
    # Настройки воркера
    MAX_CONCURRENT_TASKS: int = 5
    
    class Config:
        env_file = ".env"

settings = Settings()