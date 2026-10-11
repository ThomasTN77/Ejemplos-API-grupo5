# API Libros - Mauricio

API REST de libros hecha con FastAPI, SQLAlchemy y PostgreSQL en Neon.

## Video de evidencia (Parcial 3)

PEGAR_AQUI_EL_LINK_DEL_VIDEO

## Instalar

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

Crear un archivo `.env` con la URL de Neon (ver `.env.example`).

## Migraciones y seeders

```bash
alembic upgrade head
python -m src.seeders.seed_libros
```

## Correr la API

```bash
uvicorn main:app --reload
```

Swagger en http://127.0.0.1:8000/docs

## Endpoints

| Metodo | Ruta | Respuesta correcta | Errores |
|---|---|---|---|
| GET | /libros | 200 | 500 si falla la base de datos |
| GET | /libros/{id} | 200 | 404 si no existe |
| POST | /libros | 201 | 422 si faltan campos o son invalidos |
| PUT | /libros/{id} | 200 | 404 si no existe, 422 si los datos son invalidos |
| DELETE | /libros/{id} | 204 | 404 si no existe |

## Pruebas con Pytest

Las pruebas usan SQLite en memoria, asi que no tocan la base de datos de Neon.

```bash
python -m pytest
```

Son 10 pruebas en `tests/test_libros.py`, una normal y una de error por cada endpoint:

| Endpoint | Prueba normal | Prueba de error |
|---|---|---|
| GET /libros | `test_listar_libros_ok` (200 y la lista) | `test_listar_libros_error_base_de_datos` (500 controlado) |
| GET /libros/{id} | `test_obtener_libro_por_id_ok` (200) | `test_obtener_libro_inexistente` (404) |
| POST /libros | `test_crear_libro_ok` (201) | `test_crear_libro_sin_titulo` (422, campo faltante) |
| PUT /libros/{id} | `test_actualizar_libro_ok` (200) | `test_actualizar_libro_anio_invalido` (422, tipo incorrecto) |
| DELETE /libros/{id} | `test_eliminar_libro_ok` (204) | `test_eliminar_libro_inexistente` (404) |

Para correr una sola prueba:

```bash
python -m pytest -k test_crear_libro_ok
python -m pytest -k test_obtener_libro_inexistente
```

## Docker

Con el `.env` creado:

```bash
docker compose up --build
```

O sin compose:

```bash
docker build -t api-libros .
docker run --rm -p 8000:8000 --env-file .env api-libros
```

La API queda en http://localhost:8000/docs

## CI/CD

- `ci.yml`: corre pylint en los pull requests del grupo.
- `cd_mauricio.yml` tiene tres etapas:
  1. **pruebas**: instala dependencias, corre pylint y las 10 pruebas de Pytest.
  2. **docker**: construye la imagen, corre las pruebas dentro de la imagen y levanta la API en un contenedor para comprobar que responde.
  3. **despliegue**: se ejecuta con cada push a `feat-cicd-mauricio` o `main`. Con la imagen Docker aplica las migraciones y el seeder en Neon.

Si una etapa falla, las siguientes no se ejecutan.
