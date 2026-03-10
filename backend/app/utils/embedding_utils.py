"""
  filename      : embedding_utils
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.core.config import settings
from typing import Optional

'''
Embedding模型初始化
'''

#全局向量模型(单例模式，避免重复初始化)
_EMBEDDING_MODEL: Optional[HuggingFaceEmbeddings] = None
def get_embedding_model()->HuggingFaceEmbeddings:
    """
    获取Embedding模型实例（bge-small-zh-v1.5），单例模式
    """
    global _EMBEDDING_MODEL
    if _EMBEDDING_MODEL is None:
        _EMBEDDING_MODEL = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL_PATH,
            model_kwargs={"device": "cpu"},  # 生产环境可改为"cuda"
            encode_kwargs={"normalize_embeddings": True}  # 归一化提升检索精度
        )
        return _EMBEDDING_MODEL
