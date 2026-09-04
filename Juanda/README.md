# API de Motos

API REST construida con Python, FastAPI, SQLAlchemy y PostgreSQL en Neon. Es una adaptacion del ejemplo de animales, usando `motos` como entidad.

## Requisitos

- Python 3.11 o superior
- Una base de datos PostgreSQL en Neon (opcional para ejecutar localmente)

## Instalacion

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuracion

Para usar SQLite local, no necesitas configurar nada: se crea `motos.db` automaticamente.

Para conectar Neon, copia `.env.example` como `.env` y reemplaza `DATABASE_URL` con la cadena de conexion de tu proyecto:

```env
DATABASE_URL=postgresql://USUARIO:CONTRASENA@HOST/neondb?sslmode=require
```

La aplicacion convierte automaticamente la URL a `postgresql+psycopg` para SQLAlchemy.

## Ejecucion

```powershell
uvicorn main:app --reload
```

Abre <http://127.0.0.1:8000/docs> para probar la documentacion interactiva.

## Endpoints

- `GET /motos`: listar motos
- `GET /motos/{id}`: consultar una moto
- `POST /motos`: crear una moto
- `PUT /motos/{id}`: actualizar una moto
- `DELETE /motos/{id}`: eliminar una moto

Ejemplo para crear:

```json
{
  "marca": "Yamaha",
  "modelo": "MT-07",
  "cilindraje": 689,
  "anio": 2024
}
```
