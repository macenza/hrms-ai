from pydantic import BaseModel
from enum import Enum
from typing import Union


class UserRole(str, Enum):
    employee = "employee"
    manager = "manager"
    hr = "hr"
    admin = "admin"
    superadmin = "superadmin"
    platform_owner = "platform_owner"


class ChatRequest(BaseModel):
    user_id: Union[str, int]
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
    user_id: Union[str, int]
    role: UserRole


class NewConversationResponse(BaseModel):
    conversation_id: str


class DeleteConversationRequest(BaseModel):
    user_id: Union[str, int]
    conversation_id: str


class DeleteConversationResponse(BaseModel):
    message: str


class ConversationHistoryRequest(BaseModel):
    user_id: Union[str, int]
    conversation_id: str


class ConversationHistoryResponse(BaseModel):
    conversation_id: str
    messages: list


class RenameConversationRequest(BaseModel):
    user_id: Union[str, int]
    conversation_id: str
    title: str


class RenameConversationResponse(BaseModel):
    message: str

class ListConversationsRequest(BaseModel):
    user_id: Union[str, int]


class ListConversationsResponse(BaseModel):
    conversations: list