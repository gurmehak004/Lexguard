import ollama #type:ignore
import re

def get_llm_response(query, context):
    """Optimized: Generates answer and score in a single LLM pass."""
    
    # 1. The 'All-in-One' Prompt
    system_prompt = f"""
    You are a Research Assistant. Answer the question based ONLY on the provided context.
    
    After your answer, provide a confidence score between 0 and 1 (where 1 is perfectly 
    supported by the context and 0 is not found).
    
    FORMAT YOUR RESPONSE EXACTLY LIKE THIS:
    ANSWER: [your answer here]
    SCORE: [0.0 to 1.0]
    
    Context: {context}
    """
    
    # 2. Single Generate Call
    response = ollama.generate(
        model="llama3.2:3b",
        system=system_prompt,
        prompt=query
    )
    full_text = response['response']
    
    # 3. Parse the results using Regex (Regular Expressions)
    try:
        # Extract Answer
        answer_match = re.search(r"ANSWER:(.*?)(?=SCORE:|$)", full_text, re.DOTALL)
        answer = answer_match.group(1).strip() if answer_match else full_text
        
        # Extract Score
        score_match = re.search(r"SCORE:\s*([\d\.]+)", full_text)
        confidence = float(score_match.group(1)) if score_match else 0.5
    except Exception:
        answer = full_text
        confidence = 0.5
        
    return answer, confidence