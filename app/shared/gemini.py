import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

_groq_client = None
_gemini_client = None

def get_groq_client():
    global _groq_client
    if _groq_client is None:
        api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")
        if api_key and api_key.startswith("gsk_"):
            try:
                # pyrefly: ignore [missing-import]
                from groq import Groq
                _groq_client = Groq(api_key=api_key)
            except ImportError:
                print("Groq package is not installed.")
    return _groq_client

def get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        # Google API keys usually do not start with gsk_
        if api_key and not api_key.startswith("gsk_"):
            try:
                # pyrefly: ignore [missing-import]
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                _gemini_client = genai
            except ImportError:
                print("google-generativeai package is not installed.")
    return _gemini_client

def generate_chat_completion(prompt: str, model: str = "llama3-8b-8192", temperature: float = 0.3) -> str:
    """
    Centralized function to generate chat completions using either Groq or Google Gemini.
    Defaults to Groq as per the original codebase's implementation details.
    """
    from app.shared.database import db

    def track_token_usage(tokens_count: int):
        try:
            coll = db["ai_token_tracker"]
            coll.update_one(
                {"id": "global_budget"},
                {
                    "$inc": {"usedTokens": tokens_count},
                    "$setOnInsert": {"budget": 1000000}
                },
                upsert=True
            )
        except Exception as e:
            print(f"Error tracking token usage: {e}")

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
            if hasattr(response, 'usage') and response.usage:
                tokens = getattr(response.usage, 'total_tokens', 0)
                if tokens > 0:
                    track_token_usage(tokens)
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
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            tokens = getattr(response.usage_metadata, 'total_token_count', 0)
            if tokens > 0:
                track_token_usage(tokens)
        return response.text.strip()

    raise ValueError("No valid AI API key or client configured. Check your .env file.")
