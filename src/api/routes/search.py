from fastapi import APIRouter
from src.db.connection import PostgresClient
from src.db.repositories import ConversationRepository
from src.db.messages import MessageRepository
from src.ingestion.sec.ticker import get_company_tickers
from uuid import UUID
from pydantic import BaseModel


router = APIRouter()


