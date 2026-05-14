from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

# Step 1 - Load PDF
loader = PyPDFLoader("network.pdf")
pages = loader.load()

# Step 2 - Chunk it
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks = splitter.split_documents(pages)

# Step 3 - Create embeddings and store in ChromaDB
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print(f"Total chunks stored: {vectorstore._collection.count()}")
print("Vector store created successfully!")