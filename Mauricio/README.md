# \# API Libros - Mauricio

# 

# API de libros hecha con FastAPI, SQLAlchemy y PostgreSQL en Neon.

# 

# \## Instalar

# python -m venv .venv

# source .venv/Scripts/activate

# pip install -r requirements.txt

# 

# Crear un archivo .env con la url de Neon (ver .env.example).

# 

# \## Migraciones y seeders

# alembic upgrade head

# python -m src.seeders.seed\_libros

# 

# \## Correr la API

# uvicorn main:app --reload

# 

# Swagger en http://127.0.0.1:8000/docs

# 

# \## Endpoints

# \- GET /libros

# \- GET /libros/{id}

# \- POST /libros

# \- PUT /libros/{id}

# \- DELETE /libros/{id}

# 

# \## CI/CD

# \- ci.yml: corre pylint cuando se hace un pull request.

# \- cd\_mauricio.yml: cuando se hace merge a main corre las migraciones y el seeder en Neon.

