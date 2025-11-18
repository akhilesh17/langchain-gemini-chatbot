# chatbot_cli.py
from dotenv import load_dotenv
import os


# Import LangChain Google wrapper (adjust import if your langchain package differs)
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")


if not API_KEY:
    raise ValueError("No GOOGLE_API_KEY found in environment. Add it to .env file.")


llm = ChatGoogleGenerativeAI(
model=MODEL,
google_api_key=API_KEY,
temperature=0.2,
)


memory = ConversationBufferMemory(return_messages=True)
chain = ConversationChain(llm=llm, memory=memory)


print("CLI Chatbot (type 'exit' to quit)")
while True:
    user = input("You: ")
    if user.strip().lower() in ("exit", "quit"):
        print("Goodbye!")
        break
    resp = chain.invoke({"input": user})
    print("Bot:", resp["response"])
    