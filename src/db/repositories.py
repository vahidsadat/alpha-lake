from .connection import PostgresClient
from sqlalchemy import text
import pandas as pd
from .schemas import Conversation
from uuid import UUID
from .messages import MessageRepository

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
                        title TEXT,
                        updated_at TIMESTAMPTZ DEFAULT Now()
                    )
                    """
                )
            )

    def create_if_missing(self, session_id:UUID, title:str = None):
        insert_query = """
                            INSERT INTO alphalake.conversations (session_id, updated_at)
                            VALUES (:session_id, now())
                            ON CONFLICT (session_id) DO NOTHING;
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
                                     "title":row["title"],
                                    "updated_at":row["updated_at"]})
        return conversation

    def set_title(self, session_id:UUID, title:str):
        update_query = """
            UPDATE alphalake.conversations SET title = :title WHERE session_id = :session_id;
            """
        parameters = {"title": title, "session_id": session_id}
        with self.client.engine.begin() as connection:
                connection.execute(text(update_query), parameters)
        

    def has_title(self, session_id:UUID) -> bool:
        select_query = """
            SELECT title
            FROM alphalake.conversations
            WHERE session_id = :session_id
        """
        parameters = {"session_id": session_id}
        with self.client.engine.connect() as connection:
            result = connection.execute(text(select_query), parameters).mappings().first()
            if result and result["title"]:
                return True
            else:
                return False

    def delete_conversation(self, session_id:UUID):
        delete_query = """
            DELETE FROM alphalake.conversations WHERE session_id = :session_id;
        """
        parameters = {"session_id": session_id}
        with self.client.engine.begin() as connection:
                connection.execute(text(delete_query), parameters)