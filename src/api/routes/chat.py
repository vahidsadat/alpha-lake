from fastapi import APIRouter
from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict
from ...ai.chat_service import process_message


router = APIRouter()

class ChatRequest(BaseModel):
    session_id: UUID
    message : str

class ChatResponse(BaseModel):
    answer : str

conversation : Dict[UUID, List[ChatRequest]] = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_process_message(request:ChatRequest):
    conversation.update(request.session_id,request.message)
    answer =  process_message(request.message)


    return ChatResponse(answer=answer)
    