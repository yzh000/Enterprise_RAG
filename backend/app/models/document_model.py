"""
  filename      : documents_model
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from dataclasses import dataclass
from datetime import datetime

# 文档元数据模型
@dataclass
class DocumentMetadata:
    doc_id: str         # 文档唯一ID
    kb_id: str          # 所属知识库ID
    filename: str       # 文件名
    file_type: str      # 文件类型（pdf/docx/txt）
    size: int           # 文件大小（字节）
    page_count: int = 0 # 页码数
    upload_time: datetime = datetime.now()  # 上传时间