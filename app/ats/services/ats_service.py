import json
import time
from app.shared.gemini import generate_chat_completion
from app.shared.utils import clean_json_response
from app.shared.prompts import ATS_ANALYSIS_PROMPT

def analyze_resume(resume_text: str) -> dict:
    """
    Analyzes the resume text against industry standards using the centralized Gemini client.
    Includes retry logic for rate-limited API responses (429).
    """
    prompt = ATS_ANALYSIS_PROMPT.format(resume_text=resume_text)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            content = generate_chat_completion(prompt, model="llama-3.3-70b-versatile", temperature=0.3)
            return clean_json_response(content)
        except Exception as e:
            error_msg = str(e)
            # Retry on rate limit (429) errors with exponential backoff
            if ("429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower()) and attempt < max_retries - 1:
                wait_time = (attempt + 1) * 15  # 15s, 30s, 45s
                print(f"⚠️ ATS Rate limited (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            
            return {
                "ats_score": 0,
                "summary": "AI analysis unavailable",
                "matched_skills": [],
                "missing_skills": [],
                "strengths": [],
                "weaknesses": [],
                "recommendations": [],
                "top_interview_questions": [],
                "error": error_msg
            }
