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


async def get_assistant_response(
    user_id: str,
    role: str,
    conversation_id: str,
    message: str,
    context: str = ""
):
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
        {
            "conversation_id": conversation_id,
            "user_id": user_id
        }
    )

    if not conversation:
        return "Conversation not found"

    previous_messages = ""

    messages = conversation.get("messages", [])

    for chat in messages[-5:]:
        previous_messages += f"""
User: {chat.get('user_message', '')}
Assistant: {chat.get('assistant_response', '')}
"""

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

    User Message:
    {message}

    Assistant:
    """

    try:
        response = generate_chat_completion(
            prompt,
            model="llama3-8b-8192",
            temperature=0.5
        )

        db["conversations"].update_one(
            {
                "conversation_id": conversation_id,
                "user_id": user_id
            },
            {
                "$push": {
                    "messages": {
                        "user_message": message,
                        "assistant_response": response
                    }
                }
            }
        )

        return response

    except Exception as e:
        return f"Error: {str(e)}"


async def create_new_conversation(
    user_id: str,
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
    user_id: str,
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
    user_id: str,
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
    user_id: str,
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
    user_id: str
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