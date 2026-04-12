from engine.processor import process_pdfs
from engine.retrievers import get_hybrid_retriever
from engine.llm_handler import get_llm_response

def run_research_gpt(user_query):
    print(f"\n🔍 Processing query: {user_query}")
    
    # Step 1: Process PDFs (Ingestion)
    # Note: In a real app, you'd do this once and save the index, 
    # but for the demo, we'll run it to show the flow.
    chunks = process_pdfs("data/")
    
    # Step 2: Setup Hybrid Retriever
    retriever = get_hybrid_retriever(chunks)
    
    # Step 3: Retrieve relevant context
    print("📡 Retrieving context using Hybrid Search (FAISS + BM25)...")
    docs = retriever.invoke(user_query)
    context = "\n\n".join([doc.page_content for doc in docs])
    
    # Step 4: Get AI Response with Self-Evaluation
    print("🤖 Generating grounded response...")
    answer, confidence = get_llm_response(user_query, context)
    
    return {
        "answer": answer,
        "confidence": confidence,
        "sources": [doc.metadata.get("source", "Unknown") for doc in docs]
    }

if __name__ == "__main__":
    # Test a sample question
    # Make sure you have a PDF in the 'data' folder first!
    sample_query = "What is the main methodology discussed in these papers?"
    result = run_research_gpt(sample_query)
    
    print("\n" + "="*30)
    print(f"FINAL ANSWER:\n{result['answer']}")
    print(f"\nCONFIDENCE SCORE: {result['confidence']}")
    print(f"SOURCES: {list(set(result['sources']))}")
    print("="*30)

if __name__ == "__main__":
    print("🚀 Test Starting...")
    
    # 1. Test Ingestion
    try:
        chunks = process_pdfs("data/")
        print(f"✅ Step 1 Success: {len(chunks)} chunks created.")
    except Exception as e:
        print(f"❌ Step 1 Failed: {e}")
        exit()

    # 2. Test Retriever
    try:
        retriever = get_hybrid_retriever(chunks)
        print("✅ Step 2 Success: Retriever is ready.")
    except Exception as e:
        print(f"❌ Step 2 Failed: {e}")
        exit()

    # 3. Test Query
    sample_query = "What is the main methodology discussed in these papers?"
    result = run_research_gpt(sample_query)
    print(f"\nFinal Confidence: {result['confidence']}")    