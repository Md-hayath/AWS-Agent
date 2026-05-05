from langchain_openai import ChatOpenAI
from app.config import config
from utils.logger import logger

def get_llm():
    if not config.openai_api_key:
        logger.warning("OPENAI_API_KEY is not set. The agent might fail to start if it requires it.")
    
    return ChatOpenAI(
        model=config.llm_model,
        api_key=config.openai_api_key,
        temperature=0.0
    )
