from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import engine
from .models import SQLModel
from .routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Mart Notification Service", lifespan=lifespan)

app.include_router(router, prefix="/api/v1")