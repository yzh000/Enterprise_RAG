"""
  filename      : llm_service
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
import requests
from app.core.config import settings
from app.core.exceptions import LLMCallException

def call_deepseek(prompt:str) -> str:
    '''
    调用DeepSeek大模型生成回答
    :param prompt:
    :return:
    '''
    try:
        headers = {
            "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,  # 企业场景低温度，保证回答稳定
            "max_tokens": 1000
        }
        response = requests.post(
            url = f"{settings.DEEPSEEK_API_URL}/chat/completions",
            headers = headers,
            json = data,
            timeout = 30,
        )
        response.raise_for_status()  # 触发HTTP错误
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise LLMCallException(str(e))
