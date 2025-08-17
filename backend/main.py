from fastapi import FastAPI
from pydantic import BaseModel
import requests, os

app = FastAPI()

HF_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_API_KEY = os.getenv("HF_API_KEY")
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    payload = {"inputs": request.message, "parameters": {"max_new_tokens": 200, "temperature": 0.7}}
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    result = response.json()
    
    try:
        reply = result[0]["generated_text"]
    except:
        reply = "Error: Could not generate response."
    
    return {"reply": reply}