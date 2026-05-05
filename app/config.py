"""from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    openai_api_key: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_default_region: str = "us-east-1"
    llm_model: str = "gpt-4o"

    class Config:
        env_file = ".env"

config = Settings()
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")

config = Config()