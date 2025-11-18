# streamlit_app.py
# streamlit run streamlit_app.py
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = os.getenv("MODEL_NAME", "gemini-2.5-flash")


if not API_KEY:
    st.error("Set GOOGLE_API_KEY in .env and restart")
    st.stop()


if "conversation" not in st.session_state:
    llm = ChatGoogleGenerativeAI(model=MODEL, google_api_key=API_KEY)
    memory = ConversationBufferMemory(return_messages=True)
    st.session_state.conversation = ConversationChain(llm=llm, memory=memory)


st.title("Gemini + LangChain Chatbot — Streamlit")
query = st.text_input("Ask something:")
if st.button("Send") and query:
    with st.spinner("Thinking..."):
        resp = st.session_state.conversation.run(query)
    st.markdown("**Bot:** " + resp) 