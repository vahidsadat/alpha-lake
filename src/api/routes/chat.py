from fastapi import APIRouter , WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from uuid import UUID
from src.ai.chat_service import process_message
from src.db.connection import PostgresClient
from src.db.repositories import ConversationRepository
from src.db.messages import MessageRepository


router = APIRouter()

class ChatRequest(BaseModel):
    session_id: UUID
    message : str

class ChatResponse(BaseModel):
    answer : str

class WebSocketRequest(BaseModel):
    session_id: UUID
    message: str



def get_psql_client():
    return PostgresClient()


client = get_psql_client()
conversation = ConversationRepository(client)
messages = MessageRepository(client=client)
conversation.create_table()
messages.create_table()
@router.post("/v1/chat", response_model=ChatResponse)
async def chat_process_message(request:ChatRequest):
    conversation.add_conversation(request.session_id)
    
    history = messages.get_messages(request.session_id)
    
    answer =  process_message(request.message, history)
    if not answer:
        raise HTTPException(status_code=503, detail="AI Assisstant unavailable")
    messages.add_messages(request.session_id,history)


    return ChatResponse(answer=answer)

@router.websocket("/v1/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            request = WebSocketRequest(**data)
            conversation.add_conversation(request.session_id)
            history = messages.get_messages(request.session_id)
            answer = process_message(request.message, history)
            if not answer:
                await websocket.send_json(
                    {
                        "error" : "AI Assisstant unavailable"
                    }
                )
                continue
            await websocket.send_json({
                "answer" : answer
            })
            messages.add_messages(request.session_id,
                                  [
                                    {"role": "user", "content": request.message},
                                    {"role": "assistant", "content": answer}
                                  ])

    except WebSocketDisconnect:
        pass



    