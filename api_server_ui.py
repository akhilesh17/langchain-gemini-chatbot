# Run: uvicorn api_server_ui:app --reload --port 8000

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage


# ---------------------------------------------------
#   ENVIRONMENT
# ---------------------------------------------------
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")


# ---------------------------------------------------
#   SIMPLE MEMORY
# ---------------------------------------------------
class SimpleChatMemory:
    def __init__(self):
        self.messages = []

    def add_user_message(self, text):
        self.messages.append(HumanMessage(content=text))

    def add_ai_message(self, text):
        self.messages.append(AIMessage(content=text))


memory_store = {}   # {session_id: memory}


def get_memory(session_id):
    if session_id not in memory_store:
        memory_store[session_id] = SimpleChatMemory()
    return memory_store[session_id]


# ---------------------------------------------------
#   MODEL
# ---------------------------------------------------
model = ChatGoogleGenerativeAI(
    google_api_key=API_KEY,
    model=MODEL_NAME
)


# ---------------------------------------------------
#   FASTAPI APP
# ---------------------------------------------------
app = FastAPI()


class ChatRequest(BaseModel):
    session_id: str
    text: str


# ---------------------------------------------------
#   UI PAGE (Homepage)
# ---------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def ui():
    return """
    <html>
    <head>
        <title>AI Chatbot</title>
        <style>
            body { background:#eef2f5; font-family: Arial; padding:30px; }
            #chatbox {
                height: 400px; background:white; border-radius:8px;
                padding:15px; overflow-y:auto; border:1px solid #ccc;
            }
            #msg {
                width:75%; padding:10px; border-radius:6px;
                border:1px solid #999;
            }
            #sendBtn {
                padding:10px 20px; background:#007bff; color:white;
                border:none; border-radius:6px; cursor:pointer;
            }
        </style>
    </head>

    <body>
        <h2>AI Chatbot</h2>

        <div id="chatbox"></div>

        <br>
        <input id="msg" placeholder="Type your message..." />
        <button id="sendBtn" onclick="sendMessage()">Send</button>

        <script>
            const sessionId = Date.now().toString();

            async function sendMessage() {
                const msgBox = document.getElementById("msg");
                const text = msgBox.value.trim();
                if (!text) return;

                const chatbox = document.getElementById("chatbox");
                chatbox.innerHTML += "<div><b>You:</b> " + text + "</div>";

                const response = await fetch("/chat", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ session_id: sessionId, text: text })
                });

                const data = await response.json();
                chatbox.innerHTML += "<div><b>Bot:</b> " + data.reply + "</div><br>";

                msgBox.value = "";
                chatbox.scrollTop = chatbox.scrollHeight;
            }

            // ENTER key to send message
            document.getElementById("msg").addEventListener("keypress", function(event) {
                if (event.key === "Enter") {
                    event.preventDefault();
                    sendMessage();
                }
            });
        </script>

    </body>
    </html>
    """


# ---------------------------------------------------
#   CHAT ENDPOINT
# ---------------------------------------------------
@app.post("/chat")
async def chat_api(data: ChatRequest):
    memory = get_memory(data.session_id)

    memory.add_user_message(data.text)
    response = model.invoke(memory.messages)
    memory.add_ai_message(response.content)

    return {"reply": response.content}
