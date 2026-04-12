from langchain_community.vectorstores import FAISS #type:ignore
from langchain_community.retrievers import BM25Retriever #type:ignore
from langchain_huggingface import HuggingFaceEmbeddings #type:ignore

# --- THE "FORCE" IMPORT ---
try:
    # 1. Try the core-retrievers path (Newest 2026 standard)
    from langchain.retrievers.ensemble_retriever import EnsembleRetriever #type:ignore
except ImportError:
    try:
        # 2. Try the general retrievers path
        from langchain.retrievers import EnsembleRetriever #type:ignore
    except ImportError:
        try:
            # 3. Try core
            from langchain_core.retrievers import EnsembleRetriever  #type:ignore
        except ImportError:
            # 4. IF ALL ELSE FAILS: Define a dummy class so the code doesn't CRASH
            # This allows the UI to open even if the library is broken.
            print("⚠️ Warning: EnsembleRetriever not found. Falling back to single retriever.")
            EnsembleRetriever = None

def get_hybrid_retriever(chunks):
    # 1. Setup Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Setup FAISS (Semantic)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    faiss_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # 3. Setup BM25 (Keyword)
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 3
    
    # 4. Hybrid Logic with Safety Switch
    if EnsembleRetriever is not None:
        return EnsembleRetriever(
            retrievers=[faiss_retriever, bm25_retriever],
            weights=[0.7, 0.3]
        )
    
    # If Ensemble failed to import, return FAISS so the app still WORKS
    return faiss_retriever