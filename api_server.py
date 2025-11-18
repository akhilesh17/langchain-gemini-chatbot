# Run with:
# uvicorn api_server:app --reload --port 8000

from fastapi import FastAPI, Form
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# -------------------------
# Custom Conversation Memory (LCEL recommended way)
# -------------------------
class SimpleMemory:
    def __init__(self):
        self.history = []

    def add(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_as_string(self):
        return "\n".join([f"{m['role']}: {m['content']}" for m in self.history])

# Load ENV
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")

# LLM
llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=API_KEY)

# Memory
memory = SimpleMemory()

# FastAPI app
app = FastAPI()

class Query(BaseModel):
    text: str


@app.post("/chat")
async def chat_endpoint(q: Query):
    # Add user message
    memory.add("user", q.text)

    # Prepare prompt with history
    history = memory.get_as_string()
    prompt = f"{history}\nuser: {q.text}"

    # Call model
    ai_resp = llm.invoke([HumanMessage(content=prompt)])

    # Add assistant reply to memory
    memory.add("assistant", ai_resp.content)

    return {"reply": ai_resp.content}


@app.post("/chat-form")
async def chat_form(text: str = Form(...)):
    memory.add("user", text)

    history = memory.get_as_string()
    prompt = f"{history}\nuser: {text}"

    ai_resp = llm.invoke([HumanMessage(content=prompt)])

    memory.add("assistant", ai_resp.content)

    return {"reply": ai_resp.content}

@app.get("/")
async def home():
    return {"message": "Chatbot API running. Use POST /chat"}