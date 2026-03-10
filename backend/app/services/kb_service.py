"""
  filename      : kb_service
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from app.models.kb_model import KnowledgeBase
from app.schemas.kb_schema import CreateKBRequest
from app.core.exceptions import KBNotFoundException
import uuid
from datetime import datetime


