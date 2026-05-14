from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader(r"C:\Rag Pipeline\network.pdf")
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunk = text_splitter.split_documents(pages)
print(f"total pages loaded: {len(pages)}")
print(f"total chunks created: {len(chunk)}")
print (f"first chunk content preview:")
print(chunk[0].page_content[:500]) # Display the first 500 characters of the first chunk