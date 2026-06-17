from app.shared.gemini import generate_chat_completion
from app.assistant.prompts import ASSISTANT_SYSTEM_PROMPT

async def get_assistant_response(user_message: str) -> str:
    """
    Generate response for the AI Assistant by invoking the centralized Gemini client.
    """
    prompt = f"{ASSISTANT_SYSTEM_PROMPT}\n\nUser Message: {user_message}\nAssistant:"
    try:
        # Calls central completion service (which defaults to Groq llama model)
        response = generate_chat_completion(prompt, model="llama3-8b-8192", temperature=0.5)
        return response
    except Exception as e:
        return f"Sorry, I am currently unable to process your request. (Error: {str(e)})"
