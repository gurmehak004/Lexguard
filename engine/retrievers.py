import os
from langchain_community.vectorstores import FAISS #type:ignore
from langchain_community.retrievers import BM25Retriever #type:ignore
from langchain_core.embeddings import Embeddings #type:ignore
import google.generativeai as genai
from openai import OpenAI

# Custom LangChain-compliant embeddings wrapping Gemini & OpenAI APIs
class APIEmbeddings(Embeddings):
    def __init__(self, provider="Gemini", api_key=None):
        self.provider = provider
        self.api_key = api_key
        
    def embed_documents(self, texts):
        if self.provider == "Gemini":
            key = self.api_key or os.environ.get("GEMINI_API_KEY")
            genai.configure(api_key=key)
            # Use standard embedding model
            res = genai.embed_content(
                model="models/gemini-embedding-001",
                content=texts,
                task_type="retrieval_document"
            )
            # Return list of embeddings
            return res['embedding']
        elif self.provider == "OpenAI":
            key = self.api_key or os.environ.get("OPENAI_API_KEY")
            client = OpenAI(api_key=key)
            res = client.embeddings.create(
                model="text-embedding-3-small",
                input=texts
            )
            return [data.embedding for data in res.data]
        else:
            raise ValueError(f"Unknown provider for embeddings: {self.provider}")
            
    def embed_query(self, text):
        if self.provider == "Gemini":
            key = self.api_key or os.environ.get("GEMINI_API_KEY")
            genai.configure(api_key=key)
            res = genai.embed_content(
                model="models/gemini-embedding-001",
                content=text,
                task_type="retrieval_query"
            )
            return res['embedding']
        elif self.provider == "OpenAI":
            key = self.api_key or os.environ.get("OPENAI_API_KEY")
            client = OpenAI(api_key=key)
            res = client.embeddings.create(
                model="text-embedding-3-small",
                input=[text]
            )
            return res.data[0].embedding
        else:
            raise ValueError(f"Unknown provider for embeddings: {self.provider}")

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
            print("Warning: EnsembleRetriever not found. Falling back to single retriever.")
            EnsembleRetriever = None

def get_hybrid_retriever(chunks, provider="Local HF", api_key=None):
    # 1. Setup Embeddings (API or Local HF)
    has_api = False
    
    if provider == "Gemini":
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if key:
            try:
                embeddings = APIEmbeddings(provider="Gemini", api_key=key)
                # Test query to check if API key is valid
                embeddings.embed_query("test")
                has_api = True
            except Exception:
                pass
    elif provider == "OpenAI":
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if key:
            try:
                embeddings = APIEmbeddings(provider="OpenAI", api_key=key)
                embeddings.embed_query("test")
                has_api = True
            except Exception:
                pass

    if not has_api:
        # Fallback to local HF HuggingFaceEmbeddings
        from langchain_huggingface import HuggingFaceEmbeddings #type:ignore
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
    
    return faiss_retriever