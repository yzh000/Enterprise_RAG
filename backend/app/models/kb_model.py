"""
  filename      : kb_model
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from dataclasses import dataclass
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers import BM25Retriever
from datetime import datetime

#知识库内存模型
@dataclass
class KnowledgeBase:
    kb_id:str
    kb_name:str
    description:str
    vector_db:str
    keyword_retriever:BM25Retriever
    doc_count:int
    create_time:datetime.now()


