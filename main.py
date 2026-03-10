from fastapi import FastAPI
from config import settings

from api import spots

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="FastAPI backend for Skatemap",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(spots.router)

@app.get("/")
def root():
    return {"message": "API is running"}
