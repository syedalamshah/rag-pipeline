from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


result = embeddings.embed_query("What is IPv6?")

print(f"Type: {type(result)}")
print(f"Length: {len(result)}")
print(f"First 5 numbers: {result[:5]}")