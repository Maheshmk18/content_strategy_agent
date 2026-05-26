import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING", "true")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.mongo.client import connect_db, disconnect_db
from api.routers.agent import router

app = FastAPI(title="Content Strategy Agent")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    print("Database connected")
    print("LangSmith tracing enabled")
    yield
    await disconnect_db()


app.router.lifespan_context = lifespan
app.include_router(router, prefix="/api", tags=["agent"])


@app.get("/health")
async def health_check():
    return {"status": "ok"}
