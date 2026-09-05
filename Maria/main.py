from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.videojuegos import router as videojuegos_router
from src.database.database import Base, engine
from src.entities import videojuegos as _videojuegos_model


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Videojuegos - ITM 2026-2",
    description="API REST con FastAPI y PostgreSQL (Videojuegos)",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de videojuegos",
        "docs": "/docs",
        "recurso": "/videojuegos",
    }


app.include_router(videojuegos_router)
