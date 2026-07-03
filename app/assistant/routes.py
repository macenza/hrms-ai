from fastapi import APIRouter
import uuid

from app.assistant.services import (
    get_assistant_response,
    create_new_conversation,
    delete_conversation,
    get_conversation_history,
    rename_conversation,
    list_conversations
)

from app.assistant.schemas import (
    ChatRequest,
    ChatResponse,
    NewConversationRequest,
    NewConversationResponse,
    DeleteConversationRequest,
    DeleteConversationResponse,
    ConversationHistoryRequest,
    ConversationHistoryResponse,
    RenameConversationRequest,
    RenameConversationResponse,
    ListConversationsRequest,
    ListConversationsResponse
)

router = APIRouter(
    prefix="/assistant",
    tags=["Assistant"]
)


@router.get("/")
def assistant_home():
    return {
        "message": "AI Assistant Service is running"
    }


@router.post(
    "/chat",
    response_model=ChatResponse
)
async def assistant_chat(
    request: ChatRequest
):
    response_text = await get_assistant_response(
        request.user_id,
        request.role,
        request.conversation_id,
        request.message,
        request.context
    )

    return ChatResponse(
        conversation_id=request.conversation_id,
        role=request.role,
        message_id=str(uuid.uuid4()),
        response=response_text
    )


@router.post(
    "/conversation/new",
    response_model=NewConversationResponse
)
async def new_conversation(
    request: NewConversationRequest
):
    conversation_id = await create_new_conversation(
        request.user_id,
        request.role
    )

    return NewConversationResponse(
        conversation_id=conversation_id
    )


@router.delete(
    "/conversation/delete",
    response_model=DeleteConversationResponse
)
async def remove_conversation(
    request: DeleteConversationRequest
):
    message = await delete_conversation(
        request.user_id,
        request.conversation_id
    )

    return DeleteConversationResponse(
        message=message
    )


@router.post(
    "/conversation/history",
    response_model=ConversationHistoryResponse
)
async def conversation_history(
    request: ConversationHistoryRequest
):
    messages = await get_conversation_history(
        request.user_id,
        request.conversation_id
    )

    return ConversationHistoryResponse(
        conversation_id=request.conversation_id,
        messages=messages
    )


@router.patch(
    "/conversation/rename",
    response_model=RenameConversationResponse
)
async def update_conversation_name(
    request: RenameConversationRequest
):
    message = await rename_conversation(
        request.user_id,
        request.conversation_id,
        request.title
    )

    return RenameConversationResponse(
        message=message
    )


@router.post(
    "/conversation/list",
    response_model=ListConversationsResponse
)
async def get_user_conversations(
    request: ListConversationsRequest
):
    conversations = await list_conversations(
        request.user_id
    )

    return ListConversationsResponse(
        conversations=conversations
    )