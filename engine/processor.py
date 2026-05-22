import os
from langchain_community.document_loaders import PyPDFLoader # type: ignore

from langchain_text_splitters import RecursiveCharacterTextSplitter # type: ignore

def process_pdfs(data_path="data/", selected_files=None):
    """Loads PDFs from a folder and splits them into chunks."""
    all_docs = []
    
    # 1. Load selected or all PDFs from the directory
    files = selected_files if selected_files is not None else os.listdir(data_path)
    for file in files:
        if file.endswith(".pdf"):
            file_path = os.path.join(data_path, file)
            if os.path.exists(file_path):
                loader = PyPDFLoader(file_path)
                all_docs.extend(loader.load())
    
    # 2. Split into chunks
    # We use RecursiveCharacterTextSplitter because it's smarter with structure
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,   # Ideal for research papers
        chunk_overlap=200, # Keeps context across chunks
        add_start_index=True
    )
    
    chunks = text_splitter.split_documents(all_docs)
    print(f"Processed {len(all_docs)} pages into {len(chunks)} chunks.")
    return chunks

if __name__ == "__main__":
    # Test the processor locally
    # Make sure you have at least one PDF in the /data folder!
    process_pdfs()