from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de motos",
        "docs": "/docs",
        "recurso": "/motos",
    }


app.include_router(motos_router)
