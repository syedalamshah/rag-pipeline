__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="RAG Pipeline", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #ffffff; }
h1 { color: #1a1a1a; }
.stCaption, p, label { color: #555555 !important; }
.stTextInput input {
    background-color: #f5f5f5;
    color: #1a1a1a;
    border: 1px solid #cccccc;
}
.stButton button {
    background-color: #2563eb;
    color: white;
    border: none;
    border-radius: 6px;
}
.stButton button:hover {
    background-color: #1d4ed8;
}
.answer-box {
    background-color: #f8f8f8;
    border-left: 4px solid #2563eb;
    padding: 16px;
    border-radius: 8px;
    margin-bottom: 16px;
}
.question-text { color: #1e3a8a; font-weight: 600; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

st.title("Document Q&A")
st.caption("RAG Pipeline — Gemini + ChromaDB")

@st.cache_resource
def load_pipeline():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    return retriever, llm

retriever, llm = load_pipeline()

def get_answer(question):
    relevant_chunks = retriever.invoke(question)
    context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
    prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}

Answer:"""
    response = llm.invoke(prompt)
    return response.content

if "history" not in st.session_state:
    st.session_state.history = []

with st.form("query_form", clear_on_submit=True):
    query = st.text_input("Ask a question about the document:")
    submitted = st.form_submit_button("Ask")

if submitted and query:
    with st.spinner("Searching document and generating answer..."):
        answer = get_answer(query)
    st.session_state.history.append((query, answer))

for q, a in reversed(st.session_state.history):
    st.markdown(f'<div class="answer-box"><div class="question-text">Q: {q}</div>{a}</div>', unsafe_allow_html=True)