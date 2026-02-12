import os
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

# Load configuration values from environment variables
APP_NAME = os.getenv("APP_NAME")
CORS_ORIGINS = os.getenv("CORS_ORIGINS")
MODEL_ID = os.getenv("MODEL_ID")
LLM_TOKEN = os.getenv("LLM_TOKEN")
LLM_API_URL = os.getenv("LLM_API_URL")

# Initialize OpenAI client with Duke's LiteLLM proxy
client = OpenAI(
    api_key=LLM_TOKEN,
    base_url=LLM_API_URL,
)

# Create FastAPI app
app = FastAPI(title=APP_NAME)

# Enable CORS so frontend (different origin) can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models (input validation)
class EchoRequest(BaseModel):
    message: str

class ChatRequest(BaseModel):
    message: str
    system_prompt: Optional[str] = None
    temperature: Optional[float] = 0.7

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok", "app": APP_NAME, "model": MODEL_ID}

# Simple test endpoint
@app.get("/api/hello")
def hello(name: str = "world"):
    return {"greeting": f"Hello, {name}!", "source": APP_NAME}

# Echo API: returns message back
@app.post("/api/echo")
def echo(payload: EchoRequest):
    return {"you_said": payload.message, "len": len(payload.message)}

# Chat API: forwards user message to DukeGPT model
@app.post("/api/chat")
def chat(req: ChatRequest):
    """
    Chat using LLM proxy. Uses the Responses API.
    """
    system_msg = req.system_prompt or (
        "You are a friendly teaching assistant for a Docker classroom demo. Keep answers concise."
    )

    # Call DukeGPT model
    resp = client.responses.create(
        model=MODEL_ID,
        instructions=system_msg,
        input=req.message,
        temperature=req.temperature,
    )

    # Safely extract reply text
    reply = ""
    try:
        reply = resp.output[0].content[0].text
    except Exception:
        try:
            reply = getattr(resp, "output_text", "") or ""
        except Exception:
            reply = ""

    return {"reply": reply}
