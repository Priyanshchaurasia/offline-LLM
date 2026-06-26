from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    def generate():
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-coder:1.3b",
                "prompt": req.message,
                "stream": True
            },
            stream=True
        )
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    yield data["response"]

    return StreamingResponse(generate(), media_type="text/plain")

@app.get("/health")
def health():
    return {"status": "ok"}