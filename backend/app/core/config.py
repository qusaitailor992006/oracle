from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ORACLE - Autonomous Enterprise Decision Intelligence Engine"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    DATABASE_URL: str = "sqlite:///./data/oracle.db"
    
    # LLM Settings
    GROQ_API_KEY: Optional[str] = None
    GROQ_PRIMARY_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_FALLBACK_MODEL: str = "llama-3.1-8b-instant"
    GEMINI_API_KEY: Optional[str] = None
    
    # Security
    SECRET_KEY: str = "oracle-enterprise-decision-engine-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
