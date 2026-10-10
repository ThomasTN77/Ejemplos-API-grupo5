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


def _crear_animal(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/animales",
        json={"nombre": "Luna", "especie": "Perro", "edad": 4},
    )
    assert response.status_code == 201
    return response.json()


def test_listar_animales_devuelve_los_registros(client: TestClient) -> None:
    animal = _crear_animal(client)

    response = client.get("/animales")

    assert response.status_code == 200
    assert response.json() == [animal]


def test_listar_animales_sin_registros_devuelve_lista_vacia(
    client: TestClient,
) -> None:
    response = client.get("/animales")

    assert response.status_code == 200
    assert response.json() == []


def test_obtener_animal_por_id_devuelve_el_registro(client: TestClient) -> None:
    animal = _crear_animal(client)

    response = client.get(f"/animales/{animal['id']}")

    assert response.status_code == 200
    assert response.json() == animal


def test_obtener_animal_inexistente_devuelve_404(client: TestClient) -> None:
    response = client.get(f"/animales/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Animal no encontrado"}


def test_crear_animal_valido_normaliza_los_datos(client: TestClient) -> None:
    response = client.post(
        "/animales",
        json={"nombre": "  Luna  ", "especie": " Perro ", "edad": 4},
    )

    assert response.status_code == 201
    animal = response.json()
    assert animal["nombre"] == "Luna"
    assert animal["especie"] == "Perro"
    assert animal["edad"] == 4


def test_crear_animal_invalido_devuelve_422(client: TestClient) -> None:
    response = client.post(
        "/animales",
        json={"nombre": "", "especie": "Perro", "edad": -1},
    )

    assert response.status_code == 422
    assert "detail" in response.json()


def test_actualizar_animal_valido_devuelve_los_datos_actualizados(
    client: TestClient,
) -> None:
    animal = _crear_animal(client)

    response = client.put(
        f"/animales/{animal['id']}",
        json={"nombre": "Michi", "especie": "Gato", "edad": 2},
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": animal["id"],
        "nombre": "Michi",
        "especie": "Gato",
        "edad": 2,
    }


def test_actualizar_animal_inexistente_devuelve_404(client: TestClient) -> None:
    response = client.put(
        f"/animales/{uuid4()}",
        json={"nombre": "Michi", "especie": "Gato", "edad": 2},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Animal no encontrado"}


def test_eliminar_animal_existente_devuelve_204(client: TestClient) -> None:
    animal = _crear_animal(client)

    response = client.delete(f"/animales/{animal['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/animales/{animal['id']}").status_code == 404


def test_eliminar_animal_inexistente_devuelve_404(client: TestClient) -> None:
    response = client.delete(f"/animales/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Animal no encontrado"}