"""
  filename      : file_utils
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from idlelib.iomenu import encoding

from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from app.core.exceptions import DocumentProcessException
import tempfile
import os

def load_document(file_content: bytes, filename: str) -> list:
    """
    加载多格式文档，返回分块前的原始文档内容
    :param file_content: 文档二进制内容
    :param filename: 文件名（用于判断格式）
    :return: 文档内容列表（按页/按行拆分）
    """
    #创建临时文件（解决FastAPI上传文件只读的问题）
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name
    try:
        #根据文件后缀选择加载器
        if filename.endswith(",pdf"):
            loader = PyPDFLoader(temp_file_path)
        elif filename.endswith(".txt"):
            loader = TextLoader(temp_file_path, encoding="utf-8")
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(temp_file_path)
        else:
            raise DocumentProcessException(f"不支持的文件格式：{os.path.splitext(filename)[1]}")

        # 加载文档并提取内容+页码
        docs = loader.load()
        result = []
        for idx, doc in enumerate(docs):
            result.append({
                "page_content": doc.page_content.strip(),
                "metadata": {
                    "source_doc": filename,
                    "page": idx + 1  # 页码从1开始
                }
            })
        return result
    finally:
        #删除临时文件
        os.unlink(temp_file_path)


