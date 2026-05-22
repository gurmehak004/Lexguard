import sys
import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from project-level .env file
load_dotenv(override=True)

# 1. Setup paths and Page Config (MUST be at the very top)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
st.set_page_config(
    page_title="LexiGuard AI: Research Workspace", 
    page_icon="⚖️", 
    layout="wide"
)

from engine.processor import process_pdfs
from engine.retrievers import get_hybrid_retriever
from engine.llm_handler import (
    get_llm_response, 
    generate_section_summary, 
    compare_provisions, 
    generate_compliance_checklist
)

# Pre-loaded PDF papers mapping to pretty titles
PRE_LOADED_PAPERS = {
    "Delaware_LLC_Agreement_Sample.pdf": "Delaware LLC Operating Agreement",
    "Corporate_Code_of_Conduct_Policy.pdf": "Corporate Code of Conduct & Ethics Policy",
    "IRS_Tax_Instructions_Excerpt.pdf": "IRS Federal Tax Compliance Instructions",
    "Non_Disclosure_Agreement_Sample.pdf": "Mutual Non-Disclosure Agreement",
    "GDPR_Privacy_Compliance_Policy.pdf": "GDPR Privacy Compliance Policy",
    "CCPA_Consumer_Privacy_Guidelines.pdf": "CCPA Consumer Privacy Guidelines",
    "HIPAA_Security_Rule_Standard.pdf": "HIPAA Security Rule Standard",
    "Anti_Money_Laundering_AML_Policy.pdf": "Anti-Money Laundering & KYC Policy",
    "FCPA_Anti_Corruption_Guidelines.pdf": "FCPA Anti-Corruption Guidelines",
    "ERISA_Retirement_Plan_Summary.pdf": "ERISA Retirement Plan Summary",
    "OSHA_Workplace_Safety_Rules.pdf": "OSHA Workplace Safety Rules",
    "IP_Assignment_and_Invention_Agreement.pdf": "IP Assignment & Invention Agreement",
    "Joint_Venture_Agreement_Draft.pdf": "Joint Venture Agreement Draft",
    "IRS_W9_Instructional_Guide.pdf": "IRS Form W-9 Compliance Guide",
    "Form_1099_NEC_Filing_Instructions.pdf": "Form 1099-NEC Filing Instructions",
    "IRS_Audit_Survival_Best_Practices.pdf": "IRS Audit Survival Best Practices",
    "SOC_2_Type_II_Security_Standard.pdf": "SOC 2 Type II Security Standard",
    "Section_409A_Valuation_Guidelines.pdf": "IRC Section 409A Valuation Guidelines",
    "Delaware_Corporate_Bylaws_Template.pdf": "Delaware Corporate Bylaws Charter",
    "Employee_Handbook_Compliance_Summary.pdf": "Employee Handbook Compliance Summary"
}

# 2. Premium Design CSS Injections
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, .gradient-title {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Brand Sidebar Header */
    .sidebar-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-header h2 {
        margin: 0;
        font-size: 1.6rem;
        font-weight: 700;
    }
    
    .sidebar-header p {
        margin: 5px 0 0 0;
        font-size: 0.85rem;
        opacity: 0.9;
    }

    /* Metric Boxes */
    .metric-container {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        margin-bottom: 10px;
    }
    
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1E3A8A;
    }
    
    .metric-label {
        font-size: 0.8rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    /* Legal Disclaimer */
    .disclaimer-container {
        border-left: 4px solid #EAB308;
        background-color: #FEF9C3;
        color: #713F12;
        padding: 14px 18px;
        border-radius: 8px;
        font-size: 0.85rem;
        line-height: 1.4;
        margin: 15px 0;
    }
    
    /* Risk Flags & Assumptions */
    .risk-container {
        border-left: 4px solid #EF4444;
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    
    .assumption-container {
        border-left: 4px solid #3B82F6;
        background-color: #EFF6FF;
        color: #1E40AF;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 0.9rem;
        margin: 10px 0;
    }
    
    /* Citation badges */
    .citation-badge {
        display: inline-block;
        background-color: #E0F2FE;
        border: 1px solid #BAE6FD;
        color: #0369A1;
        padding: 3px 9px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    
    /* Checklist Priority Badges */
    .priority-high {
        background-color: #FEE2E2;
        color: #EF4444;
        padding: 3px 9px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.75rem;
        border: 1px solid #FCA5A5;
        display: inline-block;
    }
    
    .priority-medium {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 3px 9px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.75rem;
        border: 1px solid #FDE68A;
        display: inline-block;
    }
    
    .priority-low {
        background-color: #DCFCE7;
        color: #16A34A;
        padding: 3px 9px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 0.75rem;
        border: 1px solid #86EFAC;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "chunks" not in st.session_state:
    st.session_state.chunks = []
if "summaries" not in st.session_state:
    st.session_state.summaries = {}
if "checklists" not in st.session_state:
    st.session_state.checklists = {}
if "provider" not in st.session_state:
    st.session_state.provider = "Gemini"
if "model_name" not in st.session_state:
    st.session_state.model_name = "gemini-2.5-flash"
if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = []

# Load project keys from environment (loaded from .env)
gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
openai_key = os.environ.get("OPENAI_API_KEY", "").strip()

# 4. Sidebar: Workspace Branding & Configurations
with st.sidebar:
    st.markdown("""
        <div class="sidebar-header">
            <h2>⚖️ LexiGuard AI</h2>
            <p>Legal & Tax Research Agent</p>
        </div>
        """, unsafe_allow_html=True)
    

    
    # Dynamic list of loaded documents in the workspace
    st.header("📚 Indexed Workspace")
    
    available_files = []
    if os.path.exists("data"):
        available_files = [f for f in os.listdir("data") if f.endswith(".pdf")]
        
    if not available_files:
        st.info("No documents loaded. Use the uploader below to add PDFs.")
    else:
        for f in available_files:
            pretty_name = PRE_LOADED_PAPERS.get(f, f)
            st.markdown(f"- **{pretty_name}**")
            
    st.divider()
    
    # Drag-and-drop custom PDF uploader
    st.header("📤 Custom Documents")
    uploaded_files = st.file_uploader(
        "Upload legal/tax PDFs to workspace", 
        type=["pdf"], 
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        new_upload = False
        for uploaded_file in uploaded_files:
            file_path = os.path.join("data", uploaded_file.name)
            if not os.path.exists(file_path):
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                new_upload = True
                
        if new_upload:
            st.toast("New file(s) uploaded! Re-indexing...", icon="📤")
            st.session_state.retriever = None
            st.rerun()
            
    st.divider()
    
    if st.button("🗑️ Reset Workspace to Defaults"):
        # Delete custom uploaded files in data/
        for f in os.listdir("data"):
            if f.endswith(".pdf") and f not in PRE_LOADED_PAPERS:
                try:
                    os.remove(os.path.join("data", f))
                except Exception:
                    pass
        st.session_state.messages = []
        st.session_state.retriever = None
        st.session_state.chunks = []
        st.session_state.summaries = {}
        st.session_state.checklists = {}
        st.session_state.indexed_files = []
        st.success("Workspace reset to default sample papers! Re-indexing starting...")
        st.rerun()

# 5. Main Area layout
st.markdown("<h1 style='margin-bottom:0;'>🔬 LexiGuard AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:1.15rem; color:#64748B;'>Advanced Legal, Tax, & Compliance RAG Workspace</p>", unsafe_allow_html=True)
st.divider()

# Verify if API Key is configured in environment (.env)
active_key = gemini_key if st.session_state.provider == "Gemini" else openai_key
api_key_configured = bool(
    active_key and 
    active_key.strip() and 
    active_key != "your_gemini_api_key_here" and 
    active_key != "your_openai_api_key_here"
)

if not api_key_configured:
    st.warning("⚠️ **API Key Required**: Please configure the API Key inside the `.env` file of this project directory to activate the research assistant.")

# Create tabs
tab_chat, tab_summary, tab_compare, tab_checklist = st.tabs([
    "💬 Legal Chat & Q&A", 
    "📋 Document Summarizer", 
    "⚖️ Provision Compare", 
    "🛠️ Compliance Checklist"
])

# Auto-ingest all available papers on startup if retriever is None and API key is set
if st.session_state.retriever is None and available_files and api_key_configured:
    with st.spinner("Analyzing text layout & building search indexes in background..."):
        try:
            chunks = process_pdfs("data/", selected_files=available_files)
            st.session_state.chunks = chunks
            p = st.session_state.provider
            k = gemini_key if p == "Gemini" else openai_key
            st.session_state.retriever = get_hybrid_retriever(chunks, provider=p, api_key=k)
            st.session_state.indexed_files = available_files
            st.toast("✅ Workspace documents indexed successfully!", icon="⚖️")
        except Exception as e:
            st.error(f"Auto-Indexing Error: {e}")

# ----------------- TAB 1: LEGAL CHAT & Q&A -----------------
with tab_chat:
    st.markdown("""
    <div class="disclaimer-container">
        <strong>⚠️ Research Support Disclaimer</strong><br>
        This tool provides AI-driven legal, tax, and compliance research support based on your uploaded source documents. It is not a substitute for professional legal advice, tax opinion, or audit standards. Please verify all information against original documents and consultation with qualified experts.
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.retriever is None:
        st.info("💡 **Getting Started**: Select active research papers in the sidebar and click **Ingest & Index Selection** to load the assistant context.")
    else:
        # Display active documents being queried
        active_pretty = [PRE_LOADED_PAPERS[f] for f in st.session_state.indexed_files if f in PRE_LOADED_PAPERS]
        st.caption(f"📚 **Querying active database**: {', '.join(active_pretty)}")
        
        # Display existing message history
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
                # If assistant, show detailed parameters
                if msg["role"] == "assistant":
                    col_conf, col_src = st.columns([1, 2])
                    with col_conf:
                        st.markdown(f"""
                        <div class="metric-container">
                            <div class="metric-value">{int(msg.get('confidence', 0.5) * 100)}%</div>
                            <div class="metric-label">Grounded Confidence</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_src:
                        sources = msg.get('sources', [])
                        if sources:
                            src_html = "".join([f"<span class='citation-badge'>{s}</span>" for s in sources])
                            st.markdown(f"**Sources & Citations:**<br>{src_html}", unsafe_allow_html=True)
                        else:
                            st.markdown("**Sources & Citations:**<br><span class='citation-badge'>General Context</span>", unsafe_allow_html=True)
                    
                    # Risk flags
                    risks = msg.get('risk_flags', [])
                    if risks and risks != ["None"] and risks != []:
                        st.markdown("##### ⚠️ Risk Flags & Liabilities Identified")
                        risks_list = "".join([f"<li>{r}</li>" for r in risks])
                        st.markdown(f"""
                        <div class="risk-container">
                            <ul>{risks_list}</ul>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Assumptions
                    assumptions = msg.get('assumptions', [])
                    if assumptions and assumptions != ["None"] and assumptions != []:
                        st.markdown("##### 📋 Analysis Assumptions")
                        ass_list = "".join([f"<li>{a}</li>" for a in assumptions])
                        st.markdown(f"""
                        <div class="assumption-container">
                            <ul>{ass_list}</ul>
                        </div>
                        """, unsafe_allow_html=True)
        
        # User input
        query = st.chat_input("Ask a question about the active research papers...")
        
        if query:
            if not api_key_configured:
                st.error("Please configure your API Key in the `.env` file to run queries.")
            else:
                with st.chat_message("user"):
                    st.markdown(query)
                st.session_state.messages.append({"role": "user", "content": query})
                
                with st.spinner("Analyzing papers and citing sources..."):
                    # Step 1: Hybrid Retrieval
                    docs = st.session_state.retriever.invoke(query)
                    context = "\n\n".join([doc.page_content for doc in docs])
                    
                    # Step 2: Synthesis
                    provider = st.session_state.provider
                    api_key = gemini_key if provider == "Gemini" else openai_key
                    model_name = st.session_state.model_name
                    
                    answer, confidence, risk_flags, assumptions = get_llm_response(
                        query, context, provider, api_key, model_name
                    )
                    
                    sources = list(set([os.path.basename(doc.metadata.get('source', 'Unknown')) for doc in docs]))
                    
                    # Display AI message
                    with st.chat_message("assistant"):
                        st.markdown(answer)
                        
                        col_conf, col_src = st.columns([1, 2])
                        with col_conf:
                            st.markdown(f"""
                            <div class="metric-container">
                                <div class="metric-value">{int(confidence * 100)}%</div>
                                <div class="metric-label">Grounded Confidence</div>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_src:
                            if sources:
                                src_html = "".join([f"<span class='citation-badge'>{s}</span>" for s in sources])
                                st.markdown(f"**Sources & Citations:**<br>{src_html}", unsafe_allow_html=True)
                            else:
                                st.markdown("**Sources & Citations:**<br><span class='citation-badge'>General Context</span>", unsafe_allow_html=True)
                        
                        # Risk flags
                        if risk_flags and risk_flags != ["None"] and risk_flags != []:
                            st.markdown("##### ⚠️ Risk Flags & Liabilities Identified")
                            risks_list = "".join([f"<li>{r}</li>" for r in risk_flags])
                            st.markdown(f"""
                            <div class="risk-container">
                                <ul>{risks_list}</ul>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Assumptions
                        if assumptions and assumptions != ["None"] and assumptions != []:
                            st.markdown("##### 📋 Analysis Assumptions")
                            ass_list = "".join([f"<li>{a}</li>" for a in assumptions])
                            st.markdown(f"""
                            <div class="assumption-container">
                                <ul>{ass_list}</ul>
                            </div>
                            """, unsafe_allow_html=True)
                            
                # Add to chat memory
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "confidence": confidence,
                    "sources": sources,
                    "risk_flags": risk_flags,
                    "assumptions": assumptions
                })
                st.rerun()
        
        # Export Option for chat
        if st.session_state.messages:
            st.divider()
            
            transcript_md = "# LexiGuard AI legal Chat Report\n\n"
            transcript_md += f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            for msg in st.session_state.messages:
                r = "User" if msg["role"] == "user" else "AI Legal Assistant"
                transcript_md += f"### {r}:\n\n"
                transcript_md += f"{msg['content']}\n\n"
                if msg["role"] == "assistant":
                    transcript_md += f"**Confidence:** {int(msg.get('confidence', 0.5) * 100)}%\n\n"
                    if msg.get('sources'):
                        transcript_md += f"**Citations:** {', '.join(msg['sources'])}\n\n"
                    if msg.get('risk_flags') and msg['risk_flags'] != ["None"]:
                        transcript_md += "**Risk Flags:**\n" + "\n".join([f"- {ri}" for ri in msg['risk_flags']]) + "\n\n"
                    if msg.get('assumptions') and msg['assumptions'] != ["None"]:
                        transcript_md += "**Assumptions:**\n" + "\n".join([f"- {as_}" for as_ in msg['assumptions']]) + "\n\n"
                transcript_md += "---\n\n"
            
            st.download_button(
                label="📥 Export Chat History (Markdown)",
                data=transcript_md,
                file_name="lexiguard_chat_transcript.md",
                mime="text/markdown"
            )

# ----------------- TAB 2: DOCUMENT SUMMARIZER -----------------
with tab_summary:
    st.header("📋 Section-wise Document Summarization")
    st.write("Understand complex regulations or contracts section-by-section. Select an active document to analyze.")
    
    if not st.session_state.indexed_files:
        st.info("💡 Please ingest and index active papers in the sidebar first.")
    else:
        # Convert filenames to pretty titles for selectbox
        indexed_pretty_map = {f: PRE_LOADED_PAPERS.get(f, f) for f in st.session_state.indexed_files}
        selected_pretty_doc = st.selectbox(
            "Select Document for Analysis", 
            options=list(indexed_pretty_map.values())
        )
        # Find filename
        reverse_indexed_map = {v: k for k, v in indexed_pretty_map.items()}
        selected_doc = reverse_indexed_map[selected_pretty_doc]
        
        # Pull chunks for this document
        doc_chunks = [c for c in st.session_state.chunks if os.path.basename(c.metadata.get('source', '')) == selected_doc]
        
        if not doc_chunks:
            st.warning("No index chunks found for this document.")
        else:
            # Combine chunks to make sections (~5000 chars each)
            combined_sections = []
            current_text = ""
            for chunk in doc_chunks:
                if len(current_text) + len(chunk.page_content) > 5000:
                    combined_sections.append(current_text)
                    current_text = chunk.page_content
                else:
                    if current_text:
                        current_text += "\n\n" + chunk.page_content
                    else:
                        current_text = chunk.page_content
            if current_text:
                combined_sections.append(current_text)
            
            # Limit sections to process to keep speed and API costs reasonable
            max_sections = 5
            sections_to_process = combined_sections[:max_sections]
            
            # Generate summary trigger
            has_summaries = selected_doc in st.session_state.summaries
            
            col_btn, col_info = st.columns([1, 3])
            with col_btn:
                btn_label = "Re-analyze Document" if has_summaries else "⚡ Run Section-wise Analysis"
                run_summary = st.button(btn_label, key="btn_summary")
            with col_info:
                if len(combined_sections) > max_sections:
                    st.caption(f"Note: This is a large document ({len(combined_sections)} segments). Analyzing first {max_sections} core sections.")
            
            if run_summary:
                if not api_key_configured:
                    st.error("Please configure your API Key in the `.env` file.")
                else:
                    st.session_state.summaries[selected_doc] = []
                    prog_bar = st.progress(0.0)
                    status_text = st.empty()
                    
                    for idx, sec_text in enumerate(sections_to_process):
                        status_text.write(f"Analyzing section {idx+1} of {len(sections_to_process)}...")
                        p = st.session_state.provider
                        k = gemini_key if p == "Gemini" else openai_key
                        m = st.session_state.model_name
                        
                        summary_list = generate_section_summary(selected_doc, sec_text, p, k, m)
                        st.session_state.summaries[selected_doc].extend(summary_list)
                        
                        prog_bar.progress((idx + 1) / len(sections_to_process))
                    
                    status_text.write("✅ Document analysis complete!")
                    st.rerun()
            
            # Display summaries
            if selected_doc in st.session_state.summaries:
                sections = st.session_state.summaries[selected_doc]
                
                st.subheader(f"Analysis Breakdown: {selected_pretty_doc}")
                
                # Build download markdown
                summary_md = f"# Section-wise Analysis: {selected_pretty_doc}\n\n"
                summary_md += f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                
                for idx, sec in enumerate(sections):
                    title = sec.get("section_title", f"Section {idx+1}")
                    with st.expander(f"📂 {title}", expanded=True if idx == 0 else False):
                        st.markdown("**Executive Summary:**")
                        st.write(sec.get("summary", "No summary generated."))
                        
                        col_o, col_r = st.columns(2)
                        with col_o:
                            st.markdown("**⚖️ Key Mandates / Obligations:**")
                            obls = sec.get("obligations", [])
                            if obls:
                                for o in obls:
                                    st.markdown(f"- {o}")
                            else:
                                st.write("No major obligations extracted.")
                        with col_r:
                            st.markdown("**⚠️ Identified Section Risks:**")
                            rsks = sec.get("risks", [])
                            if rsks:
                                for r in rsks:
                                    st.markdown(f"- <span style='color:#DC2626;'>{r}</span>", unsafe_allow_html=True)
                            else:
                                st.write("No specific risks flagged.")
                                
                    # Add to report
                    summary_md += f"## {title}\n\n"
                    summary_md += f"**Summary:**\n{sec.get('summary')}\n\n"
                    summary_md += "**Obligations:**\n" + "\n".join([f"- {o}" for o in obls]) + "\n\n"
                    summary_md += "**Risks:**\n" + "\n".join([f"- {r}" for r in rsks]) + "\n\n"
                    summary_md += "---\n\n"
                
                st.divider()
                st.download_button(
                    label="📥 Export Analysis Report (Markdown)",
                    data=summary_md,
                    file_name=f"{selected_doc.replace('.pdf', '')}_section_summary.md",
                    mime="text/markdown"
                )

# ----------------- TAB 3: PROVISION COMPARE -----------------
with tab_compare:
    st.header("⚖️ Provision & Regulation Comparison")
    st.write("Compare old vs new policy provisions, tax codes, or contract clauses to assess changes and transitioning risks.")
    
    col_old, col_new = st.columns(2)
    with col_old:
        old_text = st.text_area(
            "Old Provision Text (e.g. FY 2024 clause or previous tax provision)", 
            height=220,
            placeholder="Paste old regulatory wording here..."
        )
    with col_new:
        new_text = st.text_area(
            "New Provision Text (e.g. FY 2025 clause or modified policy)", 
            height=220,
            placeholder="Paste new regulatory wording here..."
        )
        
    if st.button("⚖️ Compare Provisions"):
        if not old_text.strip() or not new_text.strip():
            st.warning("Please copy-paste both the old and new provision texts to compare.")
        elif not api_key_configured:
            st.error("Please configure your API Key in the `.env` file.")
        else:
            with st.spinner("Analyzing provisions side-by-side..."):
                p = st.session_state.provider
                k = gemini_key if p == "Gemini" else openai_key
                m = st.session_state.model_name
                
                res = compare_provisions(old_text, new_text, p, k, m)
                
                st.divider()
                
                # Render risk level
                risk = res.get("risk_level", "Medium")
                if risk.lower() == "high":
                    risk_badge = "<span class='priority-high'>HIGH</span>"
                elif risk.lower() == "low":
                    risk_badge = "<span class='priority-low'>LOW</span>"
                else:
                    risk_badge = "<span class='priority-medium'>MEDIUM</span>"
                    
                st.markdown(f"### Transition Risk: {risk_badge}", unsafe_allow_html=True)
                
                st.markdown("#### 📝 Changes Overview")
                st.write(res.get("comparison_summary", "No summary generated."))
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🔄 Key Alterations")
                    chgs = res.get("key_changes", [])
                    if chgs:
                        for c in chgs:
                            st.markdown(f"- {c}")
                    else:
                        st.write("No specific alterations found.")
                with col2:
                    st.markdown("#### 🏢 Operations & Audit Impact")
                    st.write(res.get("compliance_impact", "No impact details."))
                    
                st.markdown("#### 🛠️ Action Items for Compliance Alignment")
                acts = res.get("actions_required", [])
                if acts:
                    for a in acts:
                        st.markdown(f"- **[ ]** {a}")
                else:
                    st.write("No actions required.")
                
                # Export Comparison Report
                comp_report = f"# Regulation Comparison & Compliance Assessment\n\n"
                comp_report += f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                comp_report += f"## Transition Risk: {risk.upper()}\n\n"
                comp_report += f"### Executive Summary\n{res.get('comparison_summary')}\n\n"
                comp_report += "### Key Alterations\n" + "\n".join([f"- {c}" for c in chgs]) + "\n\n"
                comp_report += f"### Compliance Impact\n{res.get('compliance_impact')}\n\n"
                comp_report += "### Action Plan for Compliance Alignment\n" + "\n".join([f"- [ ] {a}" for a in acts]) + "\n\n"
                
                st.divider()
                st.download_button(
                    label="📥 Export Comparison Report (Markdown)",
                    data=comp_report,
                    file_name="provision_comparison_assessment.md",
                    mime="text/markdown"
                )

# ----------------- TAB 4: COMPLIANCE CHECKLIST -----------------
with tab_checklist:
    st.header("🛠️ Automated Compliance Checklist")
    st.write("Generate an audit and compliance checklist from your selected research papers.")
    
    if not st.session_state.indexed_files:
        st.info("💡 Please ingest and index active papers in the sidebar first.")
    else:
        # Convert filenames to pretty titles for selectbox
        chk_pretty_map = {f: PRE_LOADED_PAPERS.get(f, f) for f in st.session_state.indexed_files}
        selected_chk_pretty = st.selectbox(
            "Select Document for Checklist Ingestion", 
            options=list(chk_pretty_map.values()),
            key="chk_select"
        )
        
        # Find filename
        reverse_chk_map = {v: k for k, v in chk_pretty_map.items()}
        selected_chk_doc = reverse_chk_map[selected_chk_pretty]
        
        doc_chk_chunks = [c for c in st.session_state.chunks if os.path.basename(c.metadata.get('source', '')) == selected_chk_doc]
        
        if not doc_chk_chunks:
            st.warning("No chunks found. Re-index document in the sidebar.")
        else:
            # Combine chunks for scanning
            combined_chk_sections = []
            curr_text = ""
            for chunk in doc_chk_chunks:
                if len(curr_text) + len(chunk.page_content) > 5000:
                    combined_chk_sections.append(curr_text)
                    curr_text = chunk.page_content
                else:
                    if curr_text:
                        curr_text += "\n\n" + chunk.page_content
                    else:
                        curr_text = chunk.page_content
            if curr_text:
                combined_chk_sections.append(curr_text)
            
            # Restrict checklist scanning to core sections
            max_chk_sections = 4
            chk_sections_to_process = combined_chk_sections[:max_chk_sections]
            
            has_checklist = selected_chk_doc in st.session_state.checklists
            
            col_chk_btn, col_chk_info = st.columns([1, 3])
            with col_chk_btn:
                btn_chk_label = "Regenerate Checklist" if has_checklist else "⚡ Generate Checklist"
                run_checklist = st.button(btn_chk_label, key="btn_checklist")
            with col_chk_info:
                if len(combined_chk_sections) > max_chk_sections:
                    st.caption(f"Scanning first {max_chk_sections} core sections of this document for audit obligations.")
                    
            if run_checklist:
                if not api_key_configured:
                    st.error("Configure API Key in the `.env` file.")
                else:
                    st.session_state.checklists[selected_chk_doc] = []
                    prog_chk = st.progress(0.0)
                    status_chk = st.empty()
                    
                    for idx, text_block in enumerate(chk_sections_to_process):
                        status_chk.write(f"Extracting compliance tasks from section {idx+1} of {len(chk_sections_to_process)}...")
                        p = st.session_state.provider
                        k = gemini_key if p == "Gemini" else openai_key
                        m = st.session_state.model_name
                        
                        chk_items = generate_compliance_checklist(text_block, p, k, m)
                        st.session_state.checklists[selected_chk_doc].extend(chk_items)
                        prog_chk.progress((idx + 1) / len(chk_sections_to_process))
                        
                    status_chk.write("✅ Checklist extraction completed!")
                    st.rerun()
                    
            if selected_chk_doc in st.session_state.checklists:
                checklist = st.session_state.checklists[selected_chk_doc]
                
                st.subheader(f"Interactive Audit Checklist: {selected_chk_pretty}")
                st.caption("Check off items as they are audited or completed.")
                st.divider()
                
                # Display interactive items
                for i, item in enumerate(checklist):
                    priority = item.get("priority", "Medium")
                    if priority.lower() == "high":
                        p_class = "priority-high"
                    elif priority.lower() == "low":
                        p_class = "priority-low"
                    else:
                        p_class = "priority-medium"
                        
                    col_box, col_item = st.columns([1, 19])
                    with col_box:
                        st.checkbox("", key=f"checklist_check_{selected_chk_doc}_{i}")
                    with col_item:
                        st.markdown(f"**{item.get('task', 'No task name')}**", unsafe_allow_html=True)
                        st.markdown(f"Clause/Citation: `{item.get('clause', 'General')}` | Priority: <span class='{p_class}'>{priority.upper()}</span>", unsafe_allow_html=True)
                        st.markdown(f"<span style='color: #64748B;'>{item.get('rationale', '')}</span>", unsafe_allow_html=True)
                    st.divider()
                
                # CSV Export setup
                csv_rows = ["Task,Priority,Clause Reference,Rationale,Status"]
                for i, item in enumerate(checklist):
                    task = item.get('task', '').replace('"', '""')
                    priority = item.get('priority', '')
                    clause = item.get('clause', '').replace('"', '""')
                    rationale = item.get('rationale', '').replace('"', '""')
                    csv_rows.append(f'"{task}","{priority}","{clause}","{rationale}","Pending"')
                    
                csv_data = "\n".join(csv_rows)
                
                st.download_button(
                    label="📥 Export Checklist to CSV",
                    data=csv_data,
                    file_name=f"{selected_chk_doc.replace('.pdf', '')}_compliance_checklist.csv",
                    mime="text/csv"
                )