from fastapi import APIRouter , WebSocket, WebSocketDisconnect, HTTPException, Depends
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

class WebSocketRequest(BaseModel):
    session_id: UUID
    message: str

class SessionStore:
    def __init__(self):
        self.conversation : Dict[UUID, List[dict]] = {}

    def get_history(self, session_id : UUID) -> List[dict]:
        if session_id not in self.conversation:
            self.conversation[session_id] = []
        return self.conversation[session_id]

session_store = SessionStore()

def get_session_history() -> SessionStore:
    return session_store 


@router.post("/v1/chat", response_model=ChatResponse)
async def chat_process_message(request:ChatRequest, store: SessionStore= Depends(get_session_history)):
    history = store.get_history(request.session_id)
    
    answer =  process_message(request.message, history)
    if not answer:
        raise HTTPException(status_code=503, detail="AI Assisstant unavailable")
    history.append(
    {"role": "assistant", "content": answer}
)


    return ChatResponse(answer=answer)

@router.websocket("/v1/ws/chat")
async def websocket_chat(websocket: WebSocket, store: SessionStore= Depends(get_session_history)):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            request = WebSocketRequest(**data)
            history = store.get_history(request.session_id)
            answer = process_message(request.message, history)
            if not answer:
                await websocket.send_json(
                    {
                        "error" : "AI Assisstant unavailable"
                    }
                )
            await websocket.send_json({
                "answer" : answer
            })
            history.append(
            {"role": "assistant", "content": answer})
    except WebSocketDisconnect:
        pass



    