from langchain_community.document_loaders import TextLoader
# Purane wale ko hata kar ye likhein:
from langchain_text_splitters import RecursiveCharacterTextSplitter
from vectorstore.db_manager import DB_PATH, embeddings
from langchain_community.vectorstores import Chroma

def run_ingestion():
    loader = TextLoader("data/plumbing_knowledge.txt")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    
    Chroma.from_documents(chunks, embeddings, persist_directory=DB_PATH)
    print("✅ Knowledge base ingested successfully.")

if __name__ == "__main__":
    run_ingestion()