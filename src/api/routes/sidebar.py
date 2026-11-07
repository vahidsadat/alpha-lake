from fastapi import APIRouter
from src.db.connection import PostgresClient
from src.db.repositories import ConversationRepository
from src.db.messages import MessageRepository
from uuid import UUID
from pydantic import BaseModel


class ConversationTitleUpdate(BaseModel):
    title: str


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

@router.delete("/v1/conversations/{session_id}")
async def delete_conversation(session_id:UUID):
    messages.delete_messages(session_id=session_id)
    conversation.delete_conversation(session_id=session_id)
    return {"message": f"Conversation with session_id {session_id} deleted successfully."}

@router.patch("/v1/conversations/{session_id}/title")
async def update_conversation_title(session_id:UUID, title:ConversationTitleUpdate):
    conversation.set_title(session_id=session_id, title=title.title)
    return {"message": f"Title for conversation with session_id {session_id} updated successfully."}