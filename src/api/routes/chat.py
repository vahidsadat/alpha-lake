from fastapi import APIRouter , WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from uuid import UUID
import asyncio
from src.ai.chat_service import process_message, generate_title
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
# list_of_session_ids = messages.get_all_sessionids()
conversation.create_table()
messages.create_table()
# for session_id in list_of_session_ids:
#     conversation.add_title_to_conversations(session_id, generate_title(messages.get_messages(session_id)))

@router.websocket("/v1/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            request = WebSocketRequest(**data)

            history = messages.get_messages(request.session_id)
            answer = await asyncio.to_thread(process_message, request.message, history)

            if not answer:
                await websocket.send_json({"error": "AI Assistant unavailable"})
                continue

            # 1. parent row first (no-op if it already exists)
            conversation.create_if_missing(request.session_id)

            # 2. children after the parent exists
            new_messages = [
                {"role": "user", "content": request.message},
                {"role": "assistant", "content": answer},
            ]
            messages.add_messages(request.session_id, new_messages)

            # 3. reply right away, don't make the user wait for the title
            await websocket.send_json({"answer": answer})

            # 4. title only once, after the first exchange
            if not conversation.has_title(request.session_id):
                title = await asyncio.to_thread(generate_title, new_messages)
                conversation.set_title(request.session_id, title)

    except WebSocketDisconnect:
        pass



    