import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
print("GEMINI_API_KEY = ", os.getenv("GEMINI_API_KEY"))
client = Groq(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze_resume(resume_text):

    prompt = f"""
You are an advanced ATS (Applicant Tracking System) Resume Analyzer.

Your task is to carefully evaluate the candidate's resume against modern industry hiring standards.

Analyze the resume and return ONLY valid JSON.

Resume Content:
{resume_text}

Evaluation Guidelines:

1. Calculate ATS Score (0-100)
2. Generate a professional summary
3. Identify matched technical and soft skills
4. Identify missing important skills
5. List strengths
6. List weaknesses
7. Provide actionable recommendations
8. Generate interview questions based on candidate profile
9. Consider:
   - Education
   - Projects
   - Technical Skills
   - Certifications
   - Experience
   - Achievements
   - Communication Indicators

Return JSON in exactly this format:

{{
    "ats_score": 0,
    "summary": "",
    "matched_skills": [],
    "missing_skills": [],
    "strengths": [],
    "weaknesses": [],
    "recommendations": [],
    "top_interview_questions": []
}}

Rules:
- Return ONLY JSON.
- No markdown.
- No explanations.
- No extra text.
- ATS score must be between 0 and 100.
- Ensure valid JSON format.
"""

    try:

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content.strip()

        cleaned_text = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(cleaned_text)

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