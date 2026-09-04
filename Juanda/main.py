from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.motos import router as motos_router
from src.database.database import Base, engine
from src.entities import motos as _motos_model


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Motos - ITM 2026-2",
    description="API REST con FastAPI y PostgreSQL en Neon",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de motos",
        "docs": "/docs",
        "recurso": "/motos",
    }


app.include_router(motos_router)
