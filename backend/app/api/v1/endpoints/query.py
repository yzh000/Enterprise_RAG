"""
  filename      : query
  author        : 13105
  date          : 2026/3/11
  Description   : 
"""
from fastapi import APIRouter, Depends
from app.schemas.query_schema import QueryRequest, QueryResponse
from app.services.kb_service import get_kb_by_id
from app.services.retrieval_service import hybrid_retrieval
from app.services.llm_service import call_deepseek
from app.core.config import settings
from app.utils.timer_utils import timer
from app.core.config import settings



router = APIRouter(tags=["问答接口"])


@router.get("/query", response_model=QueryResponse)
async def query_kb(request: QueryRequest):
    kb = get_kb_by_id(request.kb_id)
    # 2. 混合检索（计时）
    with timer() as retrieval_timer:
        docs = hybrid_retrieval(request.question, kb.vector_db, kb.keyword_retriever)

    #拼接上下文
    context_parts = []
    docs_meta = []
    for idx, doc in enumerate(docs):
        source = doc.metadata.get("source_doc", "未知文档")
        page = doc.metadata.get("page")
        page_str = f"{page + 1}" if isinstance(page, int) else "未知"
        content = doc.page_content[:400] + ("..." if len(doc.page_content) > 400 else "")

        context_parts.append(f"【参考文档{idx + 1}】\n来源：{source}\n页码：{page_str}\n内容：{content}")
        docs_meta.append({
            "source": source,
            "page": page_str,
            "content_preview": content
        })
    context = "\n\n".join(context_parts) if context_parts else "无相关参考文档"

    #调用大模型
    from app.core.config import settings
    RAG_SYS_PROMPT = """【角色与任务】..."""  # 可移到core/config.py
    prompt = RAG_SYS_PROMPT.format(context=context, question=request.question)

    with timer() as generation_timer:
        answer = call_deepseek(prompt)
        if not answer:
            answer = "未检索到有效信息，建议调整关键词重试😊"

    # 组装响应
    return QueryResponse(
        answer=answer,
        docs=docs_meta,
        time_stats={
            "检索耗时": retrieval_timer.elapsed,
            "生成耗时": generation_timer.elapsed,
            "总耗时": retrieval_timer.elapsed + generation_timer.elapsed
        }
    )


