"""
  filename      : retrieval_service
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from app.core.config import settings
from app.core.exceptions import KBNotFoundException
import hashlib


def hybrid_retrieval(
        query:str,
        vector_db:FAISS,
        keyword_retriever: BM25Retriever,
)->list:
    """
    混合检索核心逻辑：FAISS向量+BM25关键词（拼接式混合检索）
    """

    #向量检索（语义相似）
    vector_retrieval = vector_db.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k":settings.VECTOR_RETRIEVE_K}
    )
    vector_docs = vector_retrieval.invoke(query)

    #BM25关键词检索
    keyword_docs = keyword_retriever.get_relevant_documents(query)[:settings.KEYWORD_RETRIEVE_K]


    #拼接+去重
    all_docs = vector_docs + keyword_docs
    seen = set()
    unique_docs = []

    for doc in all_docs:
        #优化去重：用内容哈希+来源文档
        content_hash = hashlib.md5(doc.page_content.encode("utf-8")).hexdigest()
        source = doc.metadata.get("source_doc", "")
        identifer = (content_hash, source)
        if identifer not in seen:
            seen.add(identifer)
            unique_docs.append(doc)

    return unique_docs[:settings.FINAL_RETRIEVE_K]#返回前N条