"""
  filename      : logging.py
  author        : 13105
  date          : 2026/3/11
  Description   : 
"""
import logging
import os
from datetime import datetime
from app.core.config import settings


def setup_logging(log_dir: str):
    """
    配置全局日志：按天分割，记录不同级别日志到文件+控制台
    """
    # 创建日志目录
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 日志文件名
    log_filename = os.path.join(log_dir, f"rag_system_{datetime.now().strftime('%Y%m%d')}.log")

    # 日志格式
    log_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 根日志器
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.INFO)

    # 文件处理器
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    file_handler.setFormatter(log_format)
    file_handler.setLevel(logging.DEBUG)  # 文件记录更详细的日志

    # 添加处理器
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # 屏蔽第三方库的DEBUG日志
    logging.getLogger("langchain").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)