"""
  filename      : kb_schema
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from pydantic import BaseModel, Field
from typing import List



# 创建知识库请求体
class CreateKBRequest(BaseModel):
    kb_name: str = Field(..., description="知识库名称", min_length=2, max_length=50)
    description: str = Field("", description="知识库描述", max_length=200)

# 知识库响应体
class KBResponse(BaseModel):
    kb_id: str = Field(..., description="知识库唯一ID")
    kb_name: str = Field(..., description="知识库名称")
    description: str = Field(..., description="知识库描述")
    doc_count: int = Field(..., description="知识库内文档数量")
    create_time: str = Field(..., description="创建时间")


