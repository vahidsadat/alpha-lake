from fastapi import APIRouter , WebSocket, WebSocketDisconnect, HTTPException
from src.db.connection import PostgresClient
from src.db.repositories import ConversationRepository
from src.db.messages import MessageRepository
from uuid import UUID

router = APIRouter()

client = PostgresClient()
conversation = ConversationRepository(client)
messages = MessageRepository(client)

@router.get("/v1/conversations")
async def populate_sidebar():
    conversations = conversation.get_conversation()
    return conversations

@router.get("/v1/conversations/{session_id}/messages")
async def get_specific_conversation(session_id:UUID):
    conversation_messages = messages.get_messages(session_id=session_id)
    return conversation_messages