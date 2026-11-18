from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.api.libros import router as libros_router
from src.database.database import Base, engine
from src.entities import libros as _libros_model


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Crea la tabla 'libros' si todavia no existe (necesario en Render).
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Libros",
    description="API REST basica con FastAPI y SQLAlchemy",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    # Permite que el frontend desplegado en Firebase consuma la API.
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(SQLAlchemyError)
async def manejar_error_bd(_request: Request, _exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Error interno de la base de datos"},
    )


@app.get("/")
def inicio():
    return {
        "mensaje": "API de libros",
        "docs": "/docs",
        "recurso": "/libros",
    }


app.include_router(libros_router)
