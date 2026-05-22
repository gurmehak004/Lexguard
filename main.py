from engine.processor import process_pdfs
from engine.retrievers import get_hybrid_retriever
from engine.llm_handler import get_llm_response

def run_research_gpt(user_query):
    print(f"\n[Processing] Query: {user_query}")
    
    # Step 1: Process PDFs (Ingestion)
    chunks = process_pdfs("data/")
    
    # Step 2: Setup Hybrid Retriever
    retriever = get_hybrid_retriever(chunks)
    
    # Step 3: Retrieve relevant context
    print("[Retrieval] Retrieving context using Hybrid Search (FAISS + BM25)...")
    docs = retriever.invoke(user_query)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Step 4: Get AI Response with Self-Evaluation
    print("[Generation] Generating grounded response...")
    answer, confidence, risk_flags, assumptions = get_llm_response(user_query, context)
    
    return {
        "answer": answer,
        "confidence": confidence,
        "risk_flags": risk_flags,
        "assumptions": assumptions,
        "sources": [doc.metadata.get("source", "Unknown") for doc in docs]
    }

if __name__ == "__main__":
    # Test a sample question
    # Make sure you have a PDF in the 'data' folder first!
    sample_query = "What is the main methodology discussed in these papers?"
    try:
        result = run_research_gpt(sample_query)
        print("\n" + "="*30)
        print(f"FINAL ANSWER:\n{result['answer']}")
        print(f"\nCONFIDENCE SCORE: {result['confidence']}")
        print(f"SOURCES: {list(set(result['sources']))}")
        print("="*30)
    except Exception as e:
        print(f"[Error] Execution failed: {e}")

if __name__ == "__main__":
    print("[Test] Starting...")
    
    # 1. Test Ingestion
    try:
        chunks = process_pdfs("data/")
        print(f"[Success] Step 1: {len(chunks)} chunks created.")
    except Exception as e:
        print(f"[Error] Step 1 Failed: {e}")
        exit()

    # 2. Test Retriever
    try:
        retriever = get_hybrid_retriever(chunks)
        print("[Success] Step 2: Retriever is ready.")
    except Exception as e:
        print(f"[Error] Step 2 Failed: {e}")
        exit()

    # 3. Test Query
    try:
        result = run_research_gpt(sample_query)
        print(f"\nFinal Confidence: {result['confidence']}")
    except Exception as e:
        print(f"[Error] Step 3 Failed: {e}")