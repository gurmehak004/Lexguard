import sys
import os
import time
import re
import streamlit as st

# 1. Setup paths and Page Config (MUST be at the very top)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
st.set_page_config(page_title="ResearchGPT", page_icon="🔬", layout="wide")

from engine.processor import process_pdfs
from engine.retrievers import get_hybrid_retriever
from engine.llm_handler import get_llm_response

# 2. Custom Styling for a Professional "Enterprise" Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 10px; margin-bottom: 10px; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #0747a6; color: white; font-weight: bold; }
    .confidence-box { 
        padding: 15px; 
        border-radius: 8px; 
        background-color: #ffffff; 
        border: 1px solid #dee2e6;
        border-left: 5px solid #0747a6;
        text-align: center;
    }
    .source-tag {
        display: inline-block;
        background-color: #e9ecef;
        padding: 2px 8px;
        border-radius: 4px;
        margin-right: 5px;
        font-size: 0.85em;
        color: #495057;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header Section
st.title("🔬 ResearchGPT: Autonomous RAG Agent")
st.caption("Hybrid Search (FAISS + BM25) | Local Llama 3.2 | Agentic Self-Evaluation")
st.divider()

# 4. Initialize Session States (Memory & Core Logic)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None

# 5. Sidebar: Document Handling & Uploads
with st.sidebar:
    st.header("📂 Document Library")
    st.write("Upload papers to build your local knowledge base.")
    
    uploaded_files = st.file_uploader("Upload Research PDFs", type="pdf", accept_multiple_files=True)
    
    if st.button("🚀 Process & Index Documents"):
        with st.spinner("Analyzing papers (Optimizing for Local CPU)..."):
            if uploaded_files:
                if not os.path.exists("data"):
                    os.makedirs("data")
                for uploaded_file in uploaded_files:
                    with open(os.path.join("data", uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
            
            try:
                # Triggers the Processor logic (Chunks) and Retriever logic (FAISS)
                chunks = process_pdfs("data/")
                st.session_state.retriever = get_hybrid_retriever(chunks)
                st.success(f"✅ Success! Indexed {len(chunks)} research chunks.")
            except Exception as e:
                st.error(f"Indexing Error: {e}")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 6. Chat Interface Flow
# Display existing conversation history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input (Bottom of the page)
query = st.chat_input("Ask a question about your uploaded research...")

if query:
    # Display user query
    with st.chat_message("user"):
        st.markdown(query)
    
    if st.session_state.retriever is None:
        st.warning("⚠️ Action Required: Please upload and index documents in the sidebar first.")
    else:
        with st.spinner("🤖 Agent is synthesizing an answer..."):
            start_time = time.time()
            
            # Step 1: Hybrid Retrieval
            docs = st.session_state.retriever.invoke(query)
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Step 2: Optimized Generation (Single-Pass)
            answer, confidence = get_llm_response(query, context)
            
            end_time = time.time()
            
            # Step 3: Display Response
            with st.chat_message("assistant"):
                st.markdown(answer)
                
                # Professional Metrics Row
                m_col1, m_col2, m_col3 = st.columns(3)
                with m_col1:
                    st.markdown(f"<div class='confidence-box'><b>Confidence</b><br>{int(confidence * 100)}%</div>", unsafe_allow_html=True)
                with m_col2:
                    st.metric("Latency", f"{round(end_time - start_time, 2)}s")
                with m_col3:
                    # Clean filename display (removes Windows paths)
                    sources = list(set([os.path.basename(doc.metadata.get('source', 'Unknown')) for doc in docs]))
                    source_html = "".join([f"<span class='source-tag'>{s}</span>" for s in sources])
                    st.markdown(f"<b>Sources:</b><br>{source_html}", unsafe_allow_html=True)

            # Step 4: Add to Memory
            st.session_state.messages.append({"role": "user", "content": query})
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # Step 5: Evidence Transparency
            with st.expander("🔍 View Grounding Evidence (Retrieved Chunks)"):
                for i, doc in enumerate(docs):
                    source_name = os.path.basename(doc.metadata.get('source', 'Unknown'))
                    st.info(f"**Chunk {i+1} from {source_name}**\n\n{doc.page_content}")