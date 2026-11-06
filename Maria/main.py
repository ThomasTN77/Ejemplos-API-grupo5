import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Asegurar que Python reconozca la carpeta 'Maria' como la raíz del paquete de importación 'src'
file_path = Path(__file__).resolve()
sys.path.append(str(file_path.parent))

from src.database.config import settings
from src.database.database import Base, engine
from src.api import videojuegos

# Crear las tablas automáticamente en Neon PostgreSQL al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Videojuegos - Módulo María",
    description="Backend FastAPI conectado a Neon PostgreSQL",
)

# Habilitar CORS para permitir peticiones desde Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videojuegos.router)


@app.get("/", tags=["Root"])
def read_root():
    return {
        "status": "online",
        "modulo": "Videojuegos",
        "autor": "María Isabel ",
    }