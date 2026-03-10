"""
  filename      : query_schema
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from pydantic import BaseModel, Field
from typing import List, Optional

from scripts.regsetup import description


#问答请求体
class QueryRequest(BaseModel):
    question:str = Field(..., description="用户提问内容", min_length=1, max_length=500)
    kb_id:str = Field(..., description="知识库ID", min_length=10, max_length=32)


#检索文档元数据响应表
class DocMetadataResponse(BaseModel):
    source:str = Field(..., description = "来源文档名")
    page:str = Field(..., description="文档页码")
    content_preview:str = Field(..., description="内容预览(前400字符)")

#问答响应体
class QueryResponse(BaseModel):
    answer: str = Field(..., description="大模型回答内容")
    docs: List[DocMetadataResponse] = Field(..., description="检索到的文档元数据")
    time_stats: dict = Field(..., description="响应时间统计（检索/生成/总耗时）")




