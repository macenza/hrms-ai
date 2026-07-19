from app.shared.gemini import generate_chat_completion
from app.assistant.prompts import (
    ASSISTANT_SYSTEM_PROMPT,
    EMPLOYEE_PROMPT,
    MANAGER_PROMPT,
    HR_PROMPT,
    ADMIN_PROMPT
)
from app.shared.database import db
import uuid
from typing import Union



async def get_assistant_response(
    user_id: Union[str, int],
    role: str,
    conversation_id: str,
    message: str,
    context: str = ""
) -> tuple[str, str | None]:
    """
    Returns a tuple of (response_text, updated_title).
    updated_title is non-None only when a new title was generated this turn.
    """
    role_prompt = ""

    if role.lower() == "employee":
        role_prompt = EMPLOYEE_PROMPT
    elif role.lower() == "manager":
        role_prompt = MANAGER_PROMPT
    elif role.lower() == "hr":
        role_prompt = HR_PROMPT
    elif role.lower() == "admin":
        role_prompt = ADMIN_PROMPT

    conversation = db["conversations"].find_one(
        {"conversation_id": conversation_id, "user_id": user_id}
    )

    if not conversation:
        return "Conversation not found", None

    previous_messages = ""

    messages = conversation.get("messages", [])
    message_count = conversation.get("message_count", len(messages))
    existing_title = conversation.get("title", "New Conversation")

    previous_messages = ""
    for chat in messages[-5:]:
        previous_messages += f"User: {chat.get('user_message', '')}\nAssistant: {chat.get('assistant_response', '')}\n"

    context_str = f"\nContext/Organization Data:\n{context}\n" if context else ""

    role_formatted = role.upper() if role.lower() == "hr" else role.capitalize()

    prompt = f"""
    {ASSISTANT_SYSTEM_PROMPT}

    {role_prompt}

    Live Data Context:
    {context}

    Previous Conversation:
    {previous_messages}

    User ID: {user_id}
    Role: {role_formatted}
    Conversation ID: {conversation_id}
    {context_str}
    User Message:
    {message}

    Assistant:
    """

    try:
        response = generate_chat_completion(
            prompt,
            model="llama-3.3-70b-versatile",
            temperature=0.5
        )

        # Increment message_count atomically and push the new message
        db["conversations"].update_one(
            {"conversation_id": conversation_id, "user_id": user_id},
            {
                "$push": {
                    "messages": {
                        "user_message": message,
                        "assistant_response": response
                    }
                },
                "$inc": {"message_count": 1}
            }
        )

        new_message_count = message_count + 1
        updated_title: str | None = None
        import asyncio

        is_first_message = (message_count == 0) or (existing_title in ("New Conversation", "", None))

        if is_first_message:
            # Synchronous await on first message: title must be ready before we return
            updated_title = await auto_generate_title(user_id, conversation_id, existing_title)
        elif new_message_count % 8 == 0:
            # Topic-shift check every 8 turns — fire-and-forget (non-blocking)
            asyncio.create_task(auto_generate_title(user_id, conversation_id, existing_title))

        return response, updated_title

    except Exception as e:
        error_str = str(e)
        # Detect Gemini / Groq quota-exceeded (HTTP 429) errors and surface a clean message
        if "429" in error_str or "quota" in error_str.lower() or "RESOURCE_EXHAUSTED" in error_str or "rate limit" in error_str.lower():
            return "__QUOTA_EXCEEDED__", None
        return f"Error: {error_str}", None


def generate_local_title(message: str) -> str:
    cleaned = message.strip()
    if cleaned.startswith('/'):
        parts = cleaned.split(None, 1)
        if len(parts) > 1:
            cleaned = parts[1].strip()
        else:
            cleaned = parts[0].replace('/', '').strip().capitalize()
    cleaned = cleaned.rstrip('?.!:,;')
    words = cleaned.split()
    new_title = " ".join(words[:5]) + "..." if len(words) > 5 else " ".join(words)
    if new_title:
        new_title = new_title[0].upper() + new_title[1:]
    else:
        new_title = "New Chat"
    if len(new_title) > 50:
        new_title = new_title[:47] + "..."
    return new_title


async def auto_generate_title(
    user_id: Union[str, int],
    conversation_id: str,
    existing_title: str = "New Conversation"
) -> str | None:
    """
    Generates or updates the conversation title using the LLM.
    Returns the new title string if it changed, or None if unchanged.
    """
    messages = []
    try:
        conv = db["conversations"].find_one(
            {"conversation_id": conversation_id, "user_id": user_id}
        )
        if not conv:
            return None

        messages = conv.get("messages", [])
        if not messages:
            return None

        # Build a compact conversation summary (last 6 turns max to keep prompt lean)
        history_lines = []
        for msg in messages[-6:]:
            u = msg.get('user_message', '').strip()
            a = msg.get('assistant_response', '').strip()
            if u:
                history_lines.append(f"User: {u}")
            if a:
                # Truncate long assistant responses to keep prompt compact
                history_lines.append(f"Assistant: {a[:300]}{'...' if len(a) > 300 else ''}")
        history_str = "\n".join(history_lines)

        prompt = f"""You are an expert at generating concise, professional conversation titles — similar to ChatGPT, Claude, or Notion AI.

Analyze the conversation below and generate the best possible title.

Rules:
- 3 to 8 words only
- Use Title Case capitalization
- Capture the PRIMARY intent/topic, not just keywords
- For HRMS topics: use names like "Employee Attendance Analytics", "Payroll Slip Request", "Leave Balance Overview"
- For bugs/fixes: include the affected feature, e.g. "Notification Popup Position Fix"
- For UI/design: e.g. "Dashboard Hero Redesign", "Earth Animation Improvements"
- NEVER use: "New Chat", "Conversation", "Untitled", "Chat", "New Conversation"
- Current title: "{existing_title}"
- If the current title already accurately describes the conversation's main topic, OR if messages are just minor follow-up clarifications on the same topic, return EXACTLY: {existing_title}
- Only update if this is the first real message, or if the topic has clearly and substantially shifted
- Output ONLY the final title. No quotes, no punctuation, no markdown, no explanation.

Conversation:
{history_str}

Title:"""

        raw = generate_chat_completion(
            prompt,
            model="llama-3.3-70b-versatile",
            temperature=0.1
        )

        new_title = raw.strip().strip('"').strip("'").strip("`").strip()

        # Strip any LLM preamble like "Title: ..."
        if ":" in new_title:
            parts = new_title.split(":", 1)
            if parts[0].strip().lower() in ("title", "proposed title", "new title", "conversation title"):
                new_title = parts[1].strip().strip('"').strip("'").strip()

        # Clamp length and reject obviously bad outputs
        if not new_title or len(new_title) > 80:
            new_title = None
        generic = {"new conversation", "new chat", "conversation", "untitled", "chat", "assistant"}
        if new_title and new_title.lower() in generic:
            new_title = None

        if new_title and new_title != existing_title:
            db["conversations"].update_one(
                {"conversation_id": conversation_id, "user_id": user_id},
                {"$set": {"title": new_title}}
            )
            print(f"[AI Title] Auto-renamed '{existing_title}' → '{new_title}' (conv: {conversation_id})")
            return new_title

        # If LLM title generation returned nothing valid, fall back to local title
        if not new_title and messages:
            first_msg = messages[0].get('user_message', '').strip()
            if first_msg:
                fallback_title = generate_local_title(first_msg)
                if fallback_title != existing_title:
                    db["conversations"].update_one(
                        {"conversation_id": conversation_id, "user_id": user_id},
                        {"$set": {"title": fallback_title}}
                    )
                    print(f"[AI Title Fallback] Auto-renamed '{existing_title}' → '{fallback_title}'")
                    return fallback_title

        return None

    except Exception as e:
        print(f"[AI Title] Failed to auto-generate title: {str(e)}")
        # FALLBACK: Local instant title generator
        try:
            if messages:
                first_msg = messages[0].get('user_message', '').strip()
                if first_msg:
                    fallback_title = generate_local_title(first_msg)
                    if fallback_title != existing_title:
                        db["conversations"].update_one(
                            {"conversation_id": conversation_id, "user_id": user_id},
                            {"$set": {"title": fallback_title}}
                        )
                        print(f"[AI Title Fallback] Auto-renamed '{existing_title}' → '{fallback_title}'")
                        return fallback_title
        except Exception as fallback_err:
            print(f"Fallback title generation failed: {fallback_err}")
        return None


async def create_new_conversation(
    user_id: Union[str, int],
    role: str
):
    conversation_id = str(uuid.uuid4())

    db["conversations"].insert_one(
        {
            "conversation_id": conversation_id,
            "title": "New Conversation",
            "user_id": user_id,
            "role": role,
            "messages": []
        }
    )

    return conversation_id


async def delete_conversation(
    user_id: Union[str, int],
    conversation_id: str
):
    result = db["conversations"].delete_one(
        {
            "conversation_id": conversation_id,
            "user_id": user_id
        }
    )

    if result.deleted_count == 0:
        return "Conversation not found"

    return "Conversation deleted successfully"


async def get_conversation_history(
    user_id: Union[str, int],
    conversation_id: str
):
    conversation = db["conversations"].find_one(
        {
            "conversation_id": conversation_id,
            "user_id": user_id
        }
    )

    if not conversation:
        return []

    return conversation.get("messages", [])


async def rename_conversation(
    user_id: Union[str, int],
    conversation_id: str,
    title: str
):
    result = db["conversations"].update_one(
        {
            "conversation_id": conversation_id,
            "user_id": user_id
        },
        {
            "$set": {
                "title": title
            }
        }
    )

    if result.matched_count == 0:
        return "Conversation not found"

    return "Conversation renamed successfully"


async def list_conversations(
    user_id: Union[str, int]
):
    conversations = db["conversations"].find(
        {
            "user_id": user_id
        },
        {
            "_id": 0,
            "conversation_id": 1,
            "title": 1
        }
    )

    return list(conversations)