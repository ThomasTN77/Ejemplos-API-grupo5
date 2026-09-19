from fastapi import FastAPI

from src.api.libros import router as libros_router

app = FastAPI(
    title="API Libros",
    description="API REST basica con FastAPI y SQLAlchemy",
    version="1.0.0",
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de libros",
        "docs": "/docs",
        "recurso": "/libros",
    }


app.include_router(libros_router)
