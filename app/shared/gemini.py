import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv(override=True)

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

def generate_chat_completion(prompt: str, model: str = "llama-3.3-70b-versatile", temperature: float = 0.3, use_grok: bool = False) -> str:
    """
    Centralized function to generate chat completions using Groq/Grok or Google Gemini.
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

    # 1. Try Grok / xAI if explicitly requested (and key is present)
    if use_grok:
        xai_key = os.getenv("GROQ_API_KEY")
        if xai_key and xai_key.startswith("xai-"):
            try:
                import requests
                headers = {
                    "Authorization": f"Bearer {xai_key}",
                    "Content-Type": "application/json"
                }
                grok_model = "grok-3-mini-fast"
                payload = {
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "model": grok_model,
                    "temperature": temperature
                }
                r = requests.post("https://api.x.ai/v1/chat/completions", json=payload, headers=headers, timeout=30)
                r.raise_for_status()
                res_data = r.json()
                content = res_data["choices"][0]["message"]["content"]
                
                usage = res_data.get("usage", {})
                tokens = usage.get("total_tokens", 0)
                if tokens > 0:
                    track_token_usage(tokens)
                    
                return content.strip()
            except Exception as e:
                print(f"Grok (xAI) API Error: {e}. Falling back to Gemini...")

        # Also support standard Groq gsk_ if requested
        groq_client = get_groq_client()
        if groq_client:
            try:
                groq_model = "llama-3.3-70b-versatile" if "grok" in model else model
                response = groq_client.chat.completions.create(
                    model=groq_model,
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

    # 2. Try Gemini (default for general assistant queries or when grok fails)
    gemini_client = get_gemini_client()
    if gemini_client:
        # Map non-Gemini model names (llama, grok, etc.) to a valid Gemini model
        gemini_model = model if model.startswith("gemini-") else "gemini-2.5-flash"
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
