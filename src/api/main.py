from fastapi import FastAPI

from .routes.health import router as health_router
from .routes.companies import router as companies_router
from .routes.chat import router as chat_router

app = FastAPI(
    title= "alphalake",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(companies_router)
app.include_router(chat_router)