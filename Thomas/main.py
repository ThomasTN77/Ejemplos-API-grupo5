from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.animales import router as animales_router
from src.database.database import Base, engine
from src.entities import animales as _animales_model


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Animales - ITM 2026-2",
    description="API REST con FastAPI y PostgreSQL",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuración de CORS para permitir la conexión desde Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de animales",
        "docs": "/docs",
        "recurso": "/animales",
    }


app.include_router(animales_router)
