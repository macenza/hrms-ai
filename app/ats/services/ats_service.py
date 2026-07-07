import json
from app.shared.gemini import generate_chat_completion
from app.shared.utils import clean_json_response
from app.shared.prompts import ATS_ANALYSIS_PROMPT

def analyze_resume(resume_text: str) -> dict:
    """
    Analyzes the resume text against industry standards using the centralized Gemini client.
    """
    prompt = ATS_ANALYSIS_PROMPT.format(resume_text=resume_text)
    
    try:
        content = generate_chat_completion(prompt, model="llama-3.3-70b-versatile", temperature=0.3)
        return clean_json_response(content)
    except Exception as e:
        return {
            "ats_score": 0,
            "summary": "AI analysis unavailable",
            "matched_skills": [],
            "missing_skills": [],
            "strengths": [],
            "weaknesses": [],
            "recommendations": [],
            "top_interview_questions": [],
            "error": str(e)
        }
