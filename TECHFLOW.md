# LexiGuard AI: Techflow & Project Overview

This document provides a comprehensive overview of **LexiGuard AI**, describing the system architecture, the technology stack, the components we built, and the step-by-step technical execution flows for each feature.

---

## 📋 What We Made

We built a premium, zero-configuration **AI Legal, Tax, & Compliance Research Assistant (LexiGuard AI)**. The workspace has the following key modules:

1. **Auto-Scanning Ingestion Engine**: Automatically scans the `data/` folder on startup, loads all PDFs, splits them into semantic chunks, and builds/updates the indexes in memory with zero manual configuration.
2. **Hybrid Ensemble Retriever**: Merges dense semantic vector search (via FAISS and Gemini embeddings) with sparse keyword matching (via BM25) in a `70/30` ratio. This ensures both conceptual legal queries and exact statutory numbers/clauses are retrieved.
3. **Structured AI Execution Engine**: Standardizes prompts to extract structured JSON responses from Google Gemini. It captures grounding confidence, risk flags, assumptions, and checklists.
4. **Custom-Designed UI Workspace**: A custom-themed Streamlit dashboard with a brand-aligned gradient header, embedded metrics, custom-styled hazard/risk alerts, and interactive checklists.
5. **Pre-Seeded Legal Library**: Contains 20 custom-generated professional PDF documents covering core corporate bylaws, LLC agreements, private agreements, tax instructions, and compliance policies.

---

## 🛠️ Technology Stack & APIs Used

* **Streamlit**: Web application framework and custom CSS rendering injection.
* **LangChain**: Orchestration framework for text loading, splitting, and retriever pipelines.
* **FAISS-CPU**: Vector database for dense semantic similarity search.
* **Rank_BM25**: Keyword search retriever for lexical pattern lookup.
* **PyPDF**: Document page extractor.
* **ReportLab**: Programmatic PDF compilation library.
* **Python-Dotenv**: Local credential secret manager.
* **AI Models**:
  - LLM: `gemini-2.5-flash` (via `google-generativeai` SDK).
  - Embeddings: `models/gemini-embedding-001` (producing 3072-dimensional vectors).
  - Backup Embeddings: `all-MiniLM-L6-v2` (local HuggingFace offline fallback).

---

## 🔗 Project Structure

```
lexguard/
├── app.py                      # Main Streamlit Frontend, custom CSS, & UI state manager
├── requirements.txt            # Python system dependencies
├── TECH_STACK_AND_LOGIC.md     # Technology stack & architectural logic
├── TECHFLOW.md                 # Detailed technical flow (this file)
├── engine/
│   ├── processor.py            # PDF parsing & text chunking logic
│   ├── retrievers.py           # Gemini/OpenAI API Embeddings & FAISS + BM25 Hybrid Retriever
│   └── llm_handler.py          # Gemini API wrappers & structured prompt engineering
├── data/                       # Workspace document storage (20 pre-seeded legal/tax PDFs)
└── scratch/
    └── generate_test_data.py   # Seeding script to compile the 20 professional PDF documents
```

---

## 🔄 Detailed Technical flows ("Techflow")

### 1. Startup & Document Auto-Ingestion
```
[App Startup]
      │
      ▼
[Scan folder "data/"] ────► (Found 20 PDF Files)
      │
      ▼
[engine/processor.py::process_pdfs]
      │   ├─► PyPDFLoader: Extract raw text & metadata from pages
      │   └─► RecursiveCharacterTextSplitter: Split text (1,000 char size, 200 overlap)
      │
      ▼
[engine/retrievers.py::get_hybrid_retriever]
      │   ├─► APIEmbeddings: Fetch dense vector embeddings from gemini-embedding-001
      │   ├─► FAISS: Build dense vector store & as_retriever(k=3)
      │   ├─► BM25Retriever: Build sparse keyword index & as_retriever(k=3)
      │   └─► EnsembleRetriever: Combine both retrievers with 70% vector / 30% keyword weights
      │
      ▼
[Session State] ──► Store Hybrid Retriever and Chunks in Streamlit session memory
```

---

### 2. Conversational Chat & Q&A
1. **Input**: User submits a question in the chat bar (e.g., *"What is the retention period for tax records under the IRS guidelines?"*).
2. **Context Retrieval**:
   - The query is passed to the **Ensemble Retriever** in `engine/retrievers.py`.
   - The retriever queries both the dense vector store (FAISS) and keyword index (BM25) to extract the **top 3** most relevant document chunks.
3. **Prompt Assembly**:
   - The retrieved text chunks are formatted into a single string (`context`).
   - A system prompt in `engine/llm_handler.py::get_llm_response` is loaded, instructing the LLM to answer *only* based on the context and respond in a structured JSON schema.
4. **Model Execution**:
   - The combined context and user query are sent to `gemini-2.5-flash` via the `call_llm` wrapper.
5. **Response Extraction**:
   - The raw JSON response is cleaned and parsed to extract:
     - `answer`: Grounded conversational text.
     - `confidence`: Grounding accuracy score.
     - `risk_flags`: List of liabilities or compliance requirements.
     - `assumptions`: Logical constraints or boundary scopes.
6. **UI Rendering**:
   - The UI parses the JSON output and displays the chat answer, confidence score, source document citation badges (extracted from chunk metadata), and custom styling blocks for identified risks (red alert box) and assumptions (blue alert box).

---

### 3. Section-Wise Document Summarizer
1. **Document Selection**: User chooses one of the 20 indexed papers.
2. **Chunk Processing**:
   - The backend retrieves all index chunks belonging to the selected document.
   - It compiles them into logical sections of approximately 5,000 characters each.
3. **Execution**:
   - For each section, the text is passed to `engine/llm_handler.py::generate_section_summary`.
   - The model is instructed to break down the section into:
     - `section_title`: Name of the clause or section.
     - `summary`: Plain-English summary.
     - `obligations`: Actionable mandates.
     - `risks`: One-sided terms or penalties.
4. **Display**:
   - The frontend renders an expander widget for each section. Inside each expander, users see the executive summary, obligations checklist, and highlighted risk items.

---

### 4. Side-by-Side Provision Comparison
1. **Input**: User pastes two distinct text provisions (e.g., *"Old clause"* and *"New clause"*).
2. **Execution**:
   - The old and new texts are passed to `engine/llm_handler.py::compare_provisions`.
   - The model calculates the differences, computes an overall transition risk rating (Low, Medium, or High), describes the operational/audit impact, and defines specific compliance action items.
3. **Display**:
   - The app displays a colored risk badge (Green for Low, Amber for Medium, Red for High) followed by structured columns highlighting alterations, impact, and a checkbox action plan.

---

### 5. Automated Compliance Checklist
1. **Document Ingestion**: User selects a document to audit.
2. **Checklist Extraction**:
   - Document sections are processed through `engine/llm_handler.py::generate_compliance_checklist`.
   - The LLM parses the legal wording, extracts raw requirements, and maps them to JSON objects containing a specific `task`, `priority` level, `clause` citation, and the legal `rationale`.
3. **Interactive Rendering**:
   - The tasks are rendered on the page as interactive checklists.
   - Priority levels are color-coded (Red for High, Yellow for Medium, Green for Low) with badges.
   - Users can check off audited tasks and download the final checklist as a formatted CSV file.
