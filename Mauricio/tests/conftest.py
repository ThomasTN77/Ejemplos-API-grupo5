# pylint: disable=wrong-import-position,redefined-outer-name
import os
from collections.abc import Generator

os.environ.setdefault("DATABASE_URL", "sqlite://")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from src.database.database import Base, get_db


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    sesion_prueba = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def get_db_prueba() -> Generator[Session, None, None]:
        db = sesion_prueba()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db_prueba

    with TestClient(app, raise_server_exceptions=False) as cliente:
        yield cliente

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def libro_creado(client: TestClient) -> dict:
    respuesta = client.post(
        "/libros",
        json={
            "titulo": "Cien anos de soledad",
            "autor": "Gabriel Garcia Marquez",
            "anio": 1967,
            "disponible": True,
        },
    )
    assert respuesta.status_code == 201
    return respuesta.json()
