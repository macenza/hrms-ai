import os
from dotenv import load_dotenv

load_dotenv()

_groq_client = None
_gemini_client = None

def get_groq_client():
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            gemini_key = os.getenv("GEMINI_API_KEY", "")
            if gemini_key.startswith("gsk_"):
                api_key = gemini_key
            
        if api_key:
            try:
                from groq import Groq
                _groq_client = Groq(api_key=api_key)
            except ImportError:
                print("Groq package is not installed.")
    return _groq_client

def get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and not api_key.startswith("gsk_"):
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                _gemini_client = genai
            except ImportError:
                print("google-generativeai package is not installed.")
    return _gemini_client

def generate_chat_completion(prompt: str, model: str = "llama-3.3-70b-versatile", temperature: float = 0.3) -> str:
    """
    Centralized function to generate chat completions using either Groq or Google Gemini.
    Defaults to Groq, and automatically falls back to Gemini if Groq encounters any issues.
    """
    # 1. Try Groq (default)
    groq_client = get_groq_client()
    if groq_client:
        try:
            response = groq_client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq API Error: {e}. Falling back to Gemini...")

    # 2. Try Gemini
    gemini_client = get_gemini_client()
    if gemini_client:
        # Map llama model to gemini model
        gemini_model = "gemini-2.5-flash" if "llama" in model else model
        model_instance = gemini_client.GenerativeModel(gemini_model)
        response = model_instance.generate_content(
            prompt,
            generation_config={"temperature": temperature}
        )
        return response.text.strip()

    raise ValueError("No valid AI API key or client configured. Check your .env file.")