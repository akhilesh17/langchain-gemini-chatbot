# Gemini & LangChain Python Chatbot Examples

This project provides a collection of Python-based chatbot examples built using Google's Gemini models and the LangChain framework. It demonstrates various ways to create and deploy chatbots, from simple command-line interfaces to web-based applications and Retrieval-Augmented Generation (RAG) systems.

## Features

*   **Multiple Interfaces:**
    *   **`chatbot_cli.py`**: A standard command-line interface (CLI) for a conversational bot.
    *   **`streamlit_app.py`**: A user-friendly web interface built with Streamlit.
    *   **`api_server.py`**: A FastAPI server that exposes chatbot functionality via a REST API.
    *   **`rag_chatbot.py`**: A more advanced CLI-based RAG chatbot that answers questions based on a provided document context.
*   **Powered by Google Gemini:** Utilizes the power of Google's Gemini family of models for generation.
*   **LangChain Integration:** Leverages various LangChain components:
    *   `ConversationChain` for managing dialogue.
    *   `ConversationBufferMemory` for remembering chat history.
    *   LangChain Expression Language (LCEL) for building a modern RAG pipeline.
*   **Vector Store:** Uses `Chroma` for local in-memory vector storage in the RAG example.
*   **Easy to Set Up:** Comes with a `requirements.txt` for quick dependency installation.

## Prerequisites

*   Python 3.8+
*   Git

## Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/akhilesh17/langchain-gemini-chatbot.git
    cd langchain-gemini-chatbot

    ```

2.  **Create and activate a virtual environment:**
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API Key:**
    *   Obtain a Google API Key from Google AI Studio.
    *   Create a file named `.env` in the root of the project directory (you can copy `.env.example`).
    *   Add your API key to the `.env` file:
        ```env
        GOOGLE_API_KEY="your_actual_google_api_key"
        MODEL_NAME="gemini-1.5-flash"
        ```

## How to Run the Chatbots

You can run any of the chatbot applications from your terminal. Make sure your virtual environment is activated.

### 1. Simple CLI Chatbot

This bot remembers the conversation history.

```bash
python chatbot_cli.py
```

### 2. Streamlit Web App

This runs a local web server with a chat interface.

```bash
streamlit run streamlit_app.py
```
Open your browser and go to the local URL provided by Streamlit (usually `http://localhost:8501`).

### 3. FastAPI Server

This starts an API server. You can interact with it using tools like `curl` or by building a frontend application.

```bash
uvicorn api_server:app --reload --port 8000
```

To test it from another terminal:
```bash
curl -X POST "http://localhost:8000/chat" \
-H "Content-Type: application/json" \
-d '{"text": "Hello, how are you?"}'
```

### 4. RAG Chatbot

This advanced chatbot uses a local vector store to answer questions based *only* on the context provided within the `rag_chatbot.py` script. The current implementation uses a small, hard-coded set of documents. You can modify the script to load your own documents.

```bash
python rag_chatbot.py
```

## Project Structure

```
├── .gitignore         # Files to be ignored by Git
├── api_server.py      # FastAPI application for a chat API
├── chatbot_cli.py     # Simple command-line conversational bot
├── rag_chatbot.py     # RAG implementation with a CLI
├── requirements.txt   # Python package dependencies
├── streamlit_app.py   # Streamlit web UI for the chatbot
└── .env.example       # Example environment file
```
