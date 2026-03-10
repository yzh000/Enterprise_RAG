"""
  filename      : document_schema
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from pydantic import BaseModel, Field
from typing import List, Optional

# 文档上传请求体（支持批量）
class DocumentUploadRequest(BaseModel):
    kb_id: str = Field(..., description="知识库ID")
    files: List[dict] = Field(..., description="文档列表，包含filename/content/page等")