"""
  filename      : document
  author        : 13105
  date          : 2026/3/11
  Description   : 
"""
from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.document_schema import DocumentUploadRequest
from app.services.document_service import process_and_add_document
from app.services.kb_service import get_kb_by_id


router = APIRouter(tags=["文档管理"])

@router.post("/upload", summary="上传文档到知识库")
async def upload_document(
    kb_id: str = Form(..., description="知识库ID"),
    file: UploadFile = File(..., description="待上传的文档（pdf/docx/txt）")
):
    """
    上传文档并处理后添加到指定知识库
    """
    # 读取文件二进制内容
    file_content = await file.read()
    # 处理文档并更新知识库
    kb = process_and_add_document(kb_id, file_content, file.filename)
    return {
        "msg": f"文档 {file.filename} 上传成功",
        "kb_id": kb.kb_id,
        "current_doc_count": kb.doc_count
    }