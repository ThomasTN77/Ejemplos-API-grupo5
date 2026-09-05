# API de Libros

API REST basica construida con Python, FastAPI y SQLAlchemy. Usa SQLite por
defecto, asi que corre sin configurar ninguna base de datos externa.

## Requisitos

- Python 3.11 o superior

## Instalacion

En Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

En Linux o macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

```bash
uvicorn main:app --reload
```

Documentacion interactiva: http://127.0.0.1:8000/docs

Ahi mismo puedes probar todos los endpoints sin necesidad de Postman.

## Endpoints

| Metodo | Ruta | Accion | Codigo exitoso |
|---|---|---|---|
| GET | `/` | Info de la API | 200 |
| GET | `/libros` | Lista todos los libros | 200 |
| GET | `/libros/{id}` | Consulta un libro | 200 |
| POST | `/libros` | Crea un libro | 201 |
| PUT | `/libros/{id}` | Actualiza un libro | 200 |
| DELETE | `/libros/{id}` | Elimina un libro | 204 |

Body de ejemplo para `POST` y `PUT`:

```json
{
  "titulo": "Cien anos de soledad",
  "autor": "Gabriel Garcia Marquez",
  "anio": 1967,
  "disponible": true
}
```

Si el id no existe, la API responde `404`. Si el body no pasa las validaciones
(titulo vacio, anio fuera de rango), responde `422`.

## Estructura del proyecto

```
api-libros/
├── main.py                  # Punto de entrada, arma la app
├── requirements.txt
├── .env.example
├── .gitignore
└── src/
    ├── api/libros.py        # Rutas HTTP
    ├── crud/libros.py       # Operaciones de base de datos
    ├── database/database.py # Conexion, sesion y Base
    ├── entities/libros.py   # Modelo SQLAlchemy (tabla)
    └── schemas/libros.py    # Modelos Pydantic (validacion)
```

La idea de separar en capas es que cada archivo tenga una sola
responsabilidad: `api` solo habla HTTP, `crud` solo habla con la base de datos,
y los dos se comunican a traves de los `schemas`.

## Base de datos

La tabla `libros` se crea automaticamente al iniciar la aplicacion.

Para usar PostgreSQL en lugar de SQLite, copia `.env.example` a `.env` y cambia
`DATABASE_URL`. No subas el archivo `.env` a Git.

## Subir a GitHub

```bash
git init
git add .
git commit -m "Primer commit: API de libros con FastAPI"
git branch -M main
git remote add origin https://github.com/USUARIO/REPO.git
git push -u origin main
```

El `.gitignore` ya excluye `.venv/`, `.env`, `*.db` y `__pycache__/`, asi que
solo se sube el codigo.
