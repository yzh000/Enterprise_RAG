"""
  filename      : document_service
  author        : 13105
  date          : 2026/3/11
  Description   : 
"""
from app.models.kb_model import KnowledgeBase
from app.services.kb_service import get_kb_by_id
from app.utils.file_utils import load_document
from app.utils.embedding_utils import get_embedding_model
from app.core.config import settings
from app.core.exceptions import DocumentProcessException
from langchain_core.documents import Document

def process_and_add_document(kb_id:str, file_content:bytes, filename:str) -> KnowledgeBase:
    '''
    处理上传的文档，并添加到知识库（更新向量库+BM25检索器）
    :param kb_id:
    :param file_content:
    :param filename:
    :return:
    '''
    kb = get_kb_by_id(kb_id)
    #加载并分块文档
    try:
        raw_docs = load_document(file_content, filename)
        if not raw_docs:
            raise DocumentProcessException("文档内容为空")
        #文档分块
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""] #中文分隔符优先
        )
        #拆分文档数据，保留元数据
        split_docs = []
        for raw_doc in raw_docs:
            splits = text_splitter.split_text(raw_doc["page_content"])
            for split in splits:
                split_docs.append(Document(
                    page_content=raw_doc["page_content"],
                    meta=raw_doc["metadata"],
                ))

        embedding_model = get_embedding_model()
        kb.vector_db.add_documents(split_docs)

        #更新BM25检索器
        all_dos = kb.vector_db.get_documents() + split_docs
        kb.keyword_retriever = kb.keyword_retriever.from_documents(all_dos)


        #更新文档计数
        kb.doc_count += 1

        return kb
    except Exception as e:
        raise DocumentProcessException(str(e))
