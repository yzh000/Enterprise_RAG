"""
  filename      : kb_service
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from app.models.kb_model import KnowledgeBase
from app.schemas.kb_schema import CreateKBRequest
from app.core.exceptions import KBNotFoundException
import uuid
from datetime import datetime
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever

# 全局知识库缓存（生产环境可替换为Redis）
KB_CACHE = {}


def create_kb(request: CreateKBRequest) -> KnowledgeBase:
    """
    创建知识库（初始化空的向量库和BM25检索器）
    """
    # 生成唯一KB ID
    kb_id = f"kb_{uuid.uuid4().hex[:8]}"
    # 初始化空的向量库（后续上传文档时填充）
    from app.utils.embedding_utils import get_embedding_model
    embedding_model = get_embedding_model()
    empty_vector_db = FAISS.from_texts(["初始化占位符"], embedding_model)
    # 初始化空的BM25检索器
    empty_keyword_retriever = BM25Retriever.from_texts(["初始化占位符"])

    # 创建知识库实例
    kb = KnowledgeBase(
        kb_id=kb_id,
        kb_name=request.kb_name,
        description=request.description,
        vector_db=empty_vector_db,
        keyword_retriever=empty_keyword_retriever,
        doc_count=0,
        create_time=datetime.now()
    )
    # 存入缓存
    KB_CACHE[kb_id] = kb
    return kb


def get_kb_by_id(kb_id: str) -> KnowledgeBase:
    """
    根据ID获取知识库（不存在则抛异常）
    """
    if kb_id not in KB_CACHE:
        raise KBNotFoundException(kb_id)
    return KB_CACHE[kb_id]


def delete_kb(kb_id: str) -> bool:
    """
    删除知识库
    """
    if kb_id in KB_CACHE:
        del KB_CACHE[kb_id]
        return True
    raise KBNotFoundException(kb_id)




