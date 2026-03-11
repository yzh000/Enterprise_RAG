"""
  filename      : kb
  author        : 13105
  date          : 2026/3/11
  Description   : 
"""
from fastapi import APIRouter, HTTPException
from app.schemas.kb_schema import CreateKBRequest, KBResponse
from app.services.kb_service import create_kb, get_kb_by_id, delete_kb
from datetime import datetime

router = APIRouter(tags=["知识库管理"])

@router.post("/create", response_model=KBResponse, summary="创建知识库")
async def create_knowledge_base(request: CreateKBRequest):
    """
    创建新的知识库，初始化空的向量库和BM25检索器
    """
    kb = create_kb(request)
    return KBResponse(
        kb_id=kb.kb_id,
        kb_name=kb.kb_name,
        description=kb.description,
        doc_count=kb.doc_count,
        create_time=kb.create_time.strftime("%Y-%m-%d %H:%M:%S")
    )


@router.get("/{kb_id}", response_model=KBResponse, summary="查询知识库信息")
async def get_knowledge_base(kb_id: str):
    """
    根据ID查询知识库详情
    """
    kb = get_kb_by_id(kb_id)
    return KBResponse(
        kb_id=kb.kb_id,
        kb_name=kb.kb_name,
        description=kb.description,
        doc_count=kb.doc_count,
        create_time=kb.create_time.strftime("%Y-%m-%d %H:%M:%S")
    )


@router.delete("/{kb_id}", summary="删除知识库")
async def delete_knowledge_base(kb_id: str):
    """
    根据ID删除知识库（清理缓存）
    """
    result = delete_kb(kb_id)
    if result:
        return {"msg": f"知识库 {kb_id} 删除成功"}
    raise HTTPException(status_code=404, detail="知识库不存在")