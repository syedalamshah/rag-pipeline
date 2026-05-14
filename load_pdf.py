import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()
loader = PyPDFLoader(r"C:\Rag Pipeline\network.pdf")
pages = loader.load()

print(f"Total pages loaded: {len(pages)}")
print(f"First page content preview:")
print(pages[0].page_content[:500]) # Display the first 500 characters of the first page