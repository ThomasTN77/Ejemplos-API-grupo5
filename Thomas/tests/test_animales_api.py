from collections.abc import Generator
from uuid import uuid4

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
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


def test_crear_y_obtener_animal(client: TestClient) -> None:
    response = client.post(
        "/animales",
        json={"nombre": "  Luna  ", "especie": " Perro ", "edad": 4},
    )

    assert response.status_code == 201
    animal = response.json()
    assert animal["nombre"] == "Luna"
    assert animal["especie"] == "Perro"
    assert animal["edad"] == 4
    assert client.get(f"/animales/{animal['id']}").json() == animal


def test_recurso_inexistente_devuelve_404(client: TestClient) -> None:
    response = client.get(f"/animales/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Animal no encontrado"}


@pytest.mark.parametrize(
    "payload",
    [
        {"nombre": "", "especie": "Perro", "edad": 4},
        {"nombre": "Luna", "especie": "Perro", "edad": -1},
        {"nombre": "Luna", "especie": "Perro", "edad": 201},
        {"nombre": "Luna", "especie": "Perro", "edad": 4, "extra": True},
    ],
)
def test_datos_invalidos_devuelven_422(
    client: TestClient,
    payload: dict[str, object],
) -> None:
    response = client.post("/animales", json=payload)

    assert response.status_code == 422
    assert "detail" in response.json()


def test_uuid_invalido_devuelve_422(client: TestClient) -> None:
    response = client.get("/animales/no-es-un-uuid")

    assert response.status_code == 422


def test_eliminar_animal_devuelve_204_y_luego_404(client: TestClient) -> None:
    created = client.post(
        "/animales",
        json={"nombre": "Michi", "especie": "Gato", "edad": 2},
    ).json()

    deleted = client.delete(f"/animales/{created['id']}")

    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(f"/animales/{created['id']}").status_code == 404