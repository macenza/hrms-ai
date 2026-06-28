from pydantic import BaseModel
from enum import Enum


class UserRole(str, Enum):
    employee = "employee"
    manager = "manager"
    hr = "hr"
    admin = "admin"


class ChatRequest(BaseModel):
    user_id: str
    role: UserRole
    conversation_id: str
    message: str
    context: str = ""


class ChatResponse(BaseModel):
    conversation_id: str
    role: str
    message_id: str
    response: str


class NewConversationRequest(BaseModel):
    user_id: str
    role: UserRole


class NewConversationResponse(BaseModel):
    conversation_id: str


class DeleteConversationRequest(BaseModel):
    user_id: str
    conversation_id: str


class DeleteConversationResponse(BaseModel):
    message: str


class ConversationHistoryRequest(BaseModel):
    user_id: str
    conversation_id: str


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    messages: list


class RenameConversationRequest(BaseModel):
    user_id: str
    conversation_id: str
    title: str


class RenameConversationResponse(BaseModel):
    message: str

class ListConversationsRequest(BaseModel):
    user_id: str


class ListConversationsResponse(BaseModel):
    conversations: list