from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://abtest:password@localhost:5432/abtest_db")
    PROJECT_NAME: str = "A/B Testing Platform API"
    API_V1_STR: str = "/api"
    
    class Config:
        env_file = ".env"

settings = Settings()
