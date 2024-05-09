from fastapi import FastAPI
from src.routes.earnings_routes import router as earnings_router

app = FastAPI()

app.include_router(earnings_router, prefix="/api/v1")