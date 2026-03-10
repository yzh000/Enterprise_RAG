"""
  filename      : extension
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from fastapi import HTTPException, status
#自定义异常，知识库不存在
class KBNotFoundException(HTTPException):
    def __init__(self, kb_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"知识库ID {kb_id} 不存在，请先创建知识库",
        )

#自定义异常：文档处理失败
class DocumentProcessException(HTTPException):
    def __init__(self, msg:str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文档处理失败：{msg}",
        )

#自定义异常：LLM调用失败
class LLMCallException(HTTPException):
    def __init__(self, msg:str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"大模型调用失败：{msg}",
        )