from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.health import router as health_router
from .routes.companies import router as companies_router
from .routes.chat import router as chat_router

app = FastAPI(
    title= "alphalake",
    version="0.1.0"
)

origins = [
    "http://localhost",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods= ["*"],
    allow_headers= ["*"]
)

app.include_router(health_router)
app.include_router(companies_router)
app.include_router(chat_router)