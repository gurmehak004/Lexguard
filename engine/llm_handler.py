import os
import json
import re
import google.generativeai as genai
from openai import OpenAI

def call_llm(system_prompt, user_prompt, provider="Gemini", api_key=None, model_name=None):
    """Unified client call to Gemini or OpenAI APIs."""
    if provider == "Gemini":
        # Configure API key (from parameter or environment variable)
        key = api_key or os.environ.get("GEMINI_API_KEY")
        if not key:
            raise ValueError("Gemini API Key is missing. Please enter it in the sidebar or set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=key)
        
        model = genai.GenerativeModel(
            model_name=model_name or "gemini-2.5-flash",
            system_instruction=system_prompt
        )
        
        response = model.generate_content(user_prompt)
        return response.text

    elif provider == "OpenAI":
        key = api_key or os.environ.get("OPENAI_API_KEY")
        if not key:
            raise ValueError("OpenAI API Key is missing. Please enter it in the sidebar or set OPENAI_API_KEY environment variable.")
        
        client = OpenAI(api_key=key)
        
        response = client.chat.completions.create(
            model=model_name or "gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        return response.choices[0].message.content

    else:
        raise ValueError(f"Unsupported provider: {provider}")

def clean_and_parse_json(text):
    """Cleans up potential markdown JSON formatting wrappers and parses it."""
    cleaned = text.strip()
    # Remove markdown code block syntax if present
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\n", "", cleaned)
        cleaned = re.sub(r"\n```$", "", cleaned)
    cleaned = cleaned.strip()
    
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback: extract the JSON object bounded by the first { and last }
        try:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start != -1 and end != -1:
                return json.loads(cleaned[start:end+1])
        except Exception:
            pass
        raise ValueError(f"Failed to parse JSON response. Raw response: {text}")

def get_llm_response(query, context, provider="Gemini", api_key=None, model_name=None):
    """Answers a legal/tax question based on document context, with grounding and metadata."""
    system_prompt = """You are a Legal, Tax, & Compliance AI Research Assistant. Your task is to provide objective, source-based analysis.
    
Answer the user's question based ONLY on the provided context. Make sure to refer to or cite specific sections, pages, articles, or clauses in the context.
You must output a single JSON object. Do NOT include any markdown code wrappers around your JSON (like ```json), just output the raw JSON text.

Expected JSON Structure:
{
  "answer": "your detailed response, citing specific clauses or sections from the context (e.g. [Page 2, Section 4.1]) where appropriate. Use bullet points or lists for readability.",
  "confidence": 0.95, // a float value between 0.0 and 1.0 indicating how strongly supported the answer is by the context.
  "risk_flags": [
    "identify any high-risk terms, ambiguities, potential compliance liabilities, or penalties mentioned in the context related to the query",
    "..."
  ],
  "assumptions": [
    "list any assumptions or constraints regarding the context or the question",
    "..."
  ]
}

If no risk flags or assumptions are present, return them as empty arrays []. Remember: you are a research assistant, not a final legal/tax opinion. Provide objective grounding.
"""

    user_prompt = f"Context:\n{context}\n\nQuestion:\n{query}"
    
    try:
        raw_text = call_llm(system_prompt, user_prompt, provider, api_key, model_name)
        data = clean_and_parse_json(raw_text)
        answer = data.get("answer", raw_text)
        confidence = float(data.get("confidence", 0.5))
        risk_flags = data.get("risk_flags", [])
        assumptions = data.get("assumptions", [])
        return answer, confidence, risk_flags, assumptions
    except Exception as e:
        return f"Error calling model: {str(e)}", 0.0, [f"Model connection failure: {str(e)}"], ["Failed to process due to execution error."]

def generate_section_summary(doc_name, text, provider="Gemini", api_key=None, model_name=None):
    """Generates a structured, section-wise analysis of a document chunk."""
    system_prompt = f"""You are a Legal & Compliance Analyst. Analyze the provided text from the document '{doc_name}' and provide a structured section breakdown.
Identify the main sections or clauses present in the text. For each section, provide:
1. Section Name / Clause Reference (e.g., Section 8.2: Indemnification)
2. Plain-language summary (explaining what it means in simple terms)
3. Key obligations or compliance requirements
4. Risk flags or warnings (if any, e.g. unusually one-sided clauses, strict deadlines, or heavy penalties)

Output your response strictly as a JSON list of objects. Do not include markdown code block wrappers.
Expected JSON Structure:
[
  {{
    "section_title": "Section Title / Number",
    "summary": "Plain-language summary of the section...",
    "obligations": ["Obligation 1", "Obligation 2"],
    "risks": ["Risk 1", "..."]
  }},
  ...
]
"""
    
    try:
        raw_text = call_llm(system_prompt, f"Text to analyze:\n{text}", provider, api_key, model_name)
        return clean_and_parse_json(raw_text)
    except Exception as e:
        return [{
            "section_title": "Analysis Error",
            "summary": f"Could not analyze section: {str(e)}",
            "obligations": [],
            "risks": ["Error processing text"]
        }]

def compare_provisions(old_text, new_text, provider="Gemini", api_key=None, model_name=None):
    """Compares an old and new provision side-by-side, detailing differences and risks."""
    system_prompt = """You are a Legal & Regulatory Compliance Expert. Compare the old provision and the new provision side-by-side.
Analyze:
1. What has changed (additions, deletions, rewording).
2. The compliance and operational impact of these changes.
3. The risk level associated with transitioning (High, Medium, Low).
4. Critical action items needed to align with the new provision.

Output your response strictly as a JSON object. Do not include markdown code block wrappers.
Expected JSON Structure:
{
  "comparison_summary": "Overall summary of the differences...",
  "risk_level": "High/Medium/Low",
  "key_changes": [
    "describe change 1...",
    "..."
  ],
  "compliance_impact": "Operational or regulatory impact description...",
  "actions_required": [
    "action 1...",
    "..."
  ]
}
"""
    
    user_prompt = f"OLD PROVISION:\n{old_text}\n\nNEW PROVISION:\n{new_text}"
    
    try:
        raw_text = call_llm(system_prompt, user_prompt, provider, api_key, model_name)
        return clean_and_parse_json(raw_text)
    except Exception as e:
        return {
            "comparison_summary": f"Could not perform comparison: {str(e)}",
            "risk_level": "Medium",
            "key_changes": ["Error processing clauses"],
            "compliance_impact": "Unknown",
            "actions_required": []
        }

def generate_compliance_checklist(text, provider="Gemini", api_key=None, model_name=None):
    """Generates an interactive compliance checklist from a document's requirements."""
    system_prompt = """You are a Corporate Compliance Auditor. Review the provided document text and extract all actionable compliance requirements, audits, or legal mandates.
For each requirement, create an actionable checklist item.

Output your response strictly as a JSON list of objects. Do not include markdown code block wrappers.
Expected JSON Structure:
[
  {
    "task": "Specific actionable checklist item (e.g. File Form 10-K within 90 days of fiscal year end)",
    "priority": "High/Medium/Low",
    "clause": "Citation/Reference from text (e.g., Section 12(b))",
    "rationale": "Briefly explain why this is required and what the penalty or risk is if not met."
  },
  ...
]
"""
    
    try:
        raw_text = call_llm(system_prompt, f"Document Text:\n{text}", provider, api_key, model_name)
        return clean_and_parse_json(raw_text)
    except Exception as e:
        return [{
            "task": f"Error generating checklist: {str(e)}",
            "priority": "High",
            "clause": "N/A",
            "rationale": "Failed to analyze document"
        }]