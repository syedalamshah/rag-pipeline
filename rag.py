from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
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

# Step 2 - Create the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

question = "What is IPv4?"

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
relevant_chunks = retriever.invoke(question)

context = "\n\n".join([chunk.page_content for chunk in relevant_chunks])
prompt = f"""Use the following context to answer the question.

Context:
{context}

Question: {question}

Answer:"""

response = llm.invoke(prompt)
print(response.content)