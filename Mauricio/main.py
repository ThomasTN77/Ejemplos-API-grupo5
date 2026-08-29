from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.libros import router as libros_router
from src.database.database import Base, engine
from src.entities import libros as _libros_model  # noqa: F401  (registra la tabla)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Libros",
    description="API REST basica con FastAPI y SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de libros",
        "docs": "/docs",
        "recurso": "/libros",
    }


app.include_router(libros_router)
