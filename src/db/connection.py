from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, Engine
import os
from dotenv import load_dotenv
load_dotenv()

class PostgresClient:
    schema_name: str ="alphalake"
    def __init__(self):
        self.engine = self._create_postgresql_engine()
        self._check_schema_exists()
    def _create_postgresql_engine(self)->Engine:
        user = os.getenv("PG_USER")
        password = os.getenv("PG_PASSWORD")
        
        
        if not user or not password:
            raise ValueError("PG_USER and PG_PASSWORD must be defined in your .env file")

        url = URL.create(
            "postgresql+psycopg2",
            username = user,
            password= password,
            host= os.getenv("PG_HOST","127.0.0.1"),
            port= int(os.getenv("PG_PORT","5432")),
            database = os.getenv("PG_DB","alphalake")
        )

        return create_engine(url, pool_pre_ping=True)



    def _check_schema_exists(self):
        with self.engine.begin() as connection:
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {self.schema_name}"))
            
    