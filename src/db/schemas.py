from typing import Literal
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class Conversation(BaseModel):
    id: UUID
    user_id : UUID | None = None
    created_at : datetime
    updated_at : datetime

class Message(BaseModel):
    id: int
    conversation_id : UUID
    role : Literal["user", "assistant", "system", "tool"]
    content :str
    created_at: datetime