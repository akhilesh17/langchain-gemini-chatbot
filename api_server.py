# api_server.py
from fastapi import FastAPI, Form
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")


if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")


llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=API_KEY)
memory = ConversationBufferMemory(return_messages=True)
chain = ConversationChain(llm=llm, memory=memory)


app = FastAPI()


class Query(BaseModel):
    text: str


@app.post("/chat")
async def chat_endpoint(q: Query):
    resp = chain.run(q.text)
    return {"reply": resp}


# simple form-based endpoint for quick testing
@app.post("/chat-form")
async def chat_form(text: str = Form(...)):
    return {"reply": chain.run(text)}


# Run with: uvicorn api_server:app --reload --port 8000