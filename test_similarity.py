from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

results = vectorstore._collection.query(
    query_texts=["What is IPv4?"],
    n_results=3,
    include=["documents", "distances"]
)

for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"Distance: {dist:.4f}")
    print(f"Chunk: {doc[:100]}")
    print("---")