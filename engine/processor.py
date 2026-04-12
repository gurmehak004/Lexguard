import os
from langchain_community.document_loaders import PyPDFLoader # type: ignore

from langchain_text_splitters import RecursiveCharacterTextSplitter # type: ignore

def process_pdfs(data_path="data/"):
    """Loads PDFs from a folder and splits them into chunks."""
    all_docs = []
    
    # 1. Load all PDFs from the directory
    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(data_path, file))
            all_docs.extend(loader.load())
    
    # 2. Split into chunks
    # We use RecursiveCharacterTextSplitter because it's smarter with structure
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Ideal for research papers
        chunk_overlap=200, # Keeps context across chunks
        add_start_index=True
    )
    
    chunks = text_splitter.split_documents(all_docs)
    print(f"✅ Processed {len(all_docs)} pages into {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    # Test the processor locally
    # Make sure you have at least one PDF in the /data folder!
    process_pdfs()