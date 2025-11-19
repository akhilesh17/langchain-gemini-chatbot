# rag_chatbot.py (PDF VERSION)

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# --- NEW IMPORTS FOR PDF HANDLING ---
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 1) Load API Key
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash") # Updated to stable model

if not API_KEY:
    raise RuntimeError("Set GOOGLE_API_KEY in .env")

# 2) Embeddings model
# We use a small, efficient local model for embeddings to save API costs/latency
emb = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 3) LOAD AND SPLIT PDF
# Ask user for the PDF path (or hardcode it: pdf_path = "document.pdf")
pdf_path = input("Enter the path to your PDF file: ").strip().strip('"')

if not os.path.exists(pdf_path):
    print(f"Error: File not found at {pdf_path}")
    exit()

print("Loading and processing PDF... this may take a moment.")

# A. Load the PDF
loader = PyPDFLoader(pdf_path)
raw_documents = loader.load()

# B. Split the text
# We split large PDFs into chunks (e.g., 1000 chars) so they fit into context windows
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True
)
chunks = text_splitter.split_documents(raw_documents)
print(f"Split PDF into {len(chunks)} chunks.")

# 4) Create Vectorstore
# We use .from_documents() instead of .from_texts() because the splitter returns Document objects
vectorstore = Chroma.from_documents(documents=chunks, embedding=emb)

# Retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# 5) LLM
llm = ChatGoogleGenerativeAI(
    model=MODEL,
    google_api_key=API_KEY,
    temperature=0.2
)

# 6) RAG Prompt
prompt = ChatPromptTemplate.from_template("""
Use ONLY the context below to answer the question.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}
""")

# 7) Define RAG LCEL pipeline
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()} 
    | prompt
    | llm
)

# 8) Chat loop
print("\n--- RAG Ready. Ask questions about your PDF ---")
print("(Type 'exit' to quit)")

while True:
    q = input("\nQ: ").strip()
    if q.lower() in ("exit", "quit"):
        break
    if not q:
        continue

    result = rag_chain.invoke(q)
    print("A:", result.content)