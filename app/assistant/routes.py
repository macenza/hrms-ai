from fastapi import APIRouter, Depends
from app.assistant.services import get_assistant_response
from app.assistant.schemas import ChatRequest, ChatResponse

router = APIRouter(prefix="/assistant", tags=["Assistant"])

@router.get("/")
def assistant_home():
    return {"message": "AI Assistant Service is running"}

@router.post("/chat", response_model=ChatResponse)
async def assistant_chat(request: ChatRequest):
    """
    Placeholder endpoint for AI Assistant chat capability.
    """
    response_text = await get_assistant_response(request.message)
    return ChatResponse(response=response_text)
