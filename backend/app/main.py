"""
  filename      : main.py
  author        : 13105
  date          : 2026/3/10
  Description   : 
"""
from typing import Union
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"}

app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}