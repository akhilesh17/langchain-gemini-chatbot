# rag_chatbot.py (UPDATED - MODERN LCEL VERSION)

from dotenv import load_dotenv
import os

load_dotenv()

# from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


# 1) Load API Key
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")

if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")


# 2) Embeddings model
emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")


# 3) Dummy documents (you will replace later)
docs = [
    {"page_content": "LangChain is a framework for building LLM apps.", "metadata": {"source": "intro"}},
    {"page_content": "Gemini is Google’s family of generative models.", "metadata": {"source": "intro2"}},
]

texts = [d["page_content"] for d in docs]

# Create FAISS vectorstore
# vectorstore = FAISS.from_texts(texts, emb)
vectorstore = Chroma.from_texts(texts, emb)

# Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# 4) LLM
llm = ChatGoogleGenerativeAI(
    model=MODEL,
    google_api_key=API_KEY,
    temperature=0.2
)


# 5) RAG Prompt
prompt = ChatPromptTemplate.from_template("""
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
""")


# 6) Define RAG LCEL pipeline
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}  
    | prompt
    | llm
)


# 7) Chat loop
print("RAG ready. Ask a question (type 'exit' to quit):")

while True:
    q = input("Q: ").strip()
    if q.lower() in ("exit", "quit"):
        break

    result = rag_chain.invoke(q)
    print("A:", result.content)
