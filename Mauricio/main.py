from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from src.api.libros import router as libros_router

app = FastAPI(
    title="API Libros",
    description="API REST basica con FastAPI y SQLAlchemy",
    version="1.0.0",
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
