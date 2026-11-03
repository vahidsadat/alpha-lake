from .connection import PostgresClient
from sqlalchemy import text
import pandas as pd
from .schemas import Conversation
from uuid import UUID

class ConversationRepository:

    def __init__(self,client:PostgresClient):
        self.client = client

    def create_table(self):
        with self.client.engine.begin() as connection:
            connection.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS alphalake.conversations
                    (
                        session_id UUID PRIMARY KEY,
                        updated_at TIMESTAMPTZ DEFAULT Now()
                    )
                    """
                )
            )

    def add_conversation(self, session_id:UUID):
        insert_query = """
                            INSERT INTO alphalake.conversations (session_id)
                            VALUES (:session_id)
                            ON CONFLICT(session_id)
                            DO NOTHING
                            """
        parameters = {"session_id": session_id}
        with self.client.engine.begin() as connection:
                connection.execute(text(insert_query), parameters)

    def get_conversation(self):
        select_query = """
            SELECT *
            FROM alphalake.conversations 
            ORDER BY updated_at DESC
        """
        conversation = []
        with self.client.engine.connect() as connection:
            result = connection.execute(text(select_query)).mappings().all()
            for row in result:
                conversation.append({"session_id":row["session_id"],
                                    "updated_at":row["updated_at"]})
        return conversation
        

