"""
  filename      : config
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    DEEPSEEK_URL: str = "https://api.deepseek.com"
    DEEPSEEK_API_KEY: str = "sk-f4aa6531f3a945ad92c3644829a3775a"
    #向量模型配置
    EMBEDDING_MODEL_PATH:str = "./bge-small-zh-v1.5"

    #文本分割配置
    CHUNK_SIZE:int=400
    CHUNK_OVERLAP: int = 40

    #存储路径配置
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    FAISS_PERSIST_DIR: str = "./faiss_db"
    LOG_DIR: str = "./logs"

    #检索配置
    VECTOR_RETRIEVE_K: int = 4
    KEYWORD_RETRIEVE_K: int = 3
    FINAL_RETRIEVE_K: int = 5

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
