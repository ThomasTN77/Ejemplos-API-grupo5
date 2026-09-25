from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from src.database.database import Base, get_db


TEST_DATABASE_URL = "sqlite://"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def moto_valida():
    return {
        "marca": "Honda",
        "modelo": "CB500F",
        "cilindraje": 471,
        "anio": 2024,
    }


def test_crear_y_obtener_moto(client):
    respuesta = client.post("/motos", json=moto_valida())

    assert respuesta.status_code == 201
    moto = respuesta.json()
    assert moto["marca"] == "Honda"
    assert UUID(moto["id"])

    respuesta_obtener = client.get(f"/motos/{moto['id']}")

    assert respuesta_obtener.status_code == 200
    assert respuesta_obtener.json() == moto


def test_rechaza_datos_invalidos(client):
    datos = {**moto_valida(), "marca": "   ", "cilindraje": 0}

    respuesta = client.post("/motos", json=datos)

    assert respuesta.status_code == 422
    assert "detail" in respuesta.json()


def test_retorna_404_para_moto_inexistente(client):
    respuesta = client.get("/motos/00000000-0000-0000-0000-000000000000")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Moto no encontrada"}


def test_actualiza_y_elimina_moto(client):
    creada = client.post("/motos", json=moto_valida()).json()
    datos_actualizados = {**moto_valida(), "modelo": "CB650R"}

    respuesta_actualizar = client.put(
        f"/motos/{creada['id']}",
        json=datos_actualizados,
    )
    respuesta_eliminar = client.delete(f"/motos/{creada['id']}")
    respuesta_final = client.get(f"/motos/{creada['id']}")

    assert respuesta_actualizar.status_code == 200
    assert respuesta_actualizar.json()["modelo"] == "CB650R"
    assert respuesta_eliminar.status_code == 204
    assert respuesta_final.status_code == 404