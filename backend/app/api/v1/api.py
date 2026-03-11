"""
  filename      : api
  author        : 13105
  date          : 2026/3/11
  Description   : 
"""
from fastapi import APIRouter
from app.api.v1.endpoints import kb, query, document


# 汇总所有v1版本的接口
api_router = APIRouter()
api_router.include_router(kb.router, prefix="/kb", tags=["知识库管理"])
api_router.include_router(query.router, prefix="/qa", tags=["问答服务"])
api_router.include_router(document.router, prefix="/document", tags=["文档管理"])