from .connection import PostgresClient
from sqlalchemy import text
from uuid import UUID


class MessageRepository:
    
    def __init__(self,client:PostgresClient):
        self.client = client

    def create_table(self):
        with self.client.engine.begin() as connection:
            connection.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS alphalake.messages
                    (
                        id BIGSERIAL PRIMARY KEY,
                        session_id UUID NOT NULL REFERENCES alphalake.conversations(session_id) ON DELETE CASCADE,
                        role VARCHAR NOT NULL CHECK (role in ('user', 'assistant', 'system', 'tool')),
                        content TEXT NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT Now()
                    )
                    """
                )
            )
    def add_messages(self,session_id: UUID, messages: list[dict]):
        insert_query = """
                            INSERT INTO alphalake.messages (session_id,role,content)
                            VALUES (:session_id,:role, :content)
                            """
        updated_query = """
                            UPDATE alphalake.conversations
                            SET updated_at = now()
                            WHERE session_id = :session_id
                        """
        
        rows = [
        {
            "session_id": session_id,
            "role": m["role"],
            "content": m["content"],
        }
        for m in messages if isinstance(m,dict)
        ]
        with self.client.engine.begin() as connection:
            connection.execute(text(insert_query), rows)
            connection.execute(text(updated_query), {"session_id": session_id})

    def get_messages(self,session_id: UUID, number_of_messages:int = 100)->list[dict]:
        N = number_of_messages
        select_query = """
                SELECT role, content
                FROM (
                    SELECT id, role, content
                    FROM alphalake.messages
                    WHERE session_id = :session_id
                    ORDER BY id DESC
                    LIMIT :N
                ) recent
                ORDER BY id ASC
            """
        parameters = {
            "session_id" : session_id,
            "N" : N
        }
        conversation = []
        with self.client.engine.connect() as connection:
            result = connection.execute(text(select_query),parameters).mappings().all()
            for row in result:
                conversation.append({"role":row["role"],
                                     "content":row["content"]})
        return conversation

            