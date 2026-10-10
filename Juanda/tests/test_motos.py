from uuid import UUID

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from src.api import motos as motos_api
from src.database.database import Base, get_db


engine = create_engine(
    "sqlite://",
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


def test_listar_motos_retorna_lista(client):
    client.post("/motos", json=moto_valida())

    respuesta = client.get("/motos")

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
    assert respuesta.json()[0]["modelo"] == "CB500F"


def test_listar_motos_maneja_error_del_repositorio(client, monkeypatch):
    def listar_con_error(_db):
        raise HTTPException(status_code=503, detail="Base de datos no disponible")

    monkeypatch.setattr(motos_api.repo, "listar", listar_con_error)

    respuesta = client.get("/motos")

    assert respuesta.status_code == 503
    assert respuesta.json() == {"detail": "Base de datos no disponible"}


def test_obtener_moto_existente(client):
    creada = client.post("/motos", json=moto_valida()).json()

    respuesta = client.get(f"/motos/{creada['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json() == creada
    assert UUID(respuesta.json()["id"])


def test_obtener_moto_inexistente_retorna_404(client):
    respuesta = client.get("/motos/00000000-0000-0000-0000-000000000000")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Moto no encontrada"}


def test_crear_moto_valida(client):
    respuesta = client.post("/motos", json=moto_valida())

    assert respuesta.status_code == 201
    assert respuesta.json()["marca"] == "Honda"
    assert UUID(respuesta.json()["id"])


def test_crear_moto_con_datos_invalidos_retorna_422(client):
    datos = {**moto_valida(), "cilindraje": 0}

    respuesta = client.post("/motos", json=datos)

    assert respuesta.status_code == 422
    assert respuesta.json()["detail"]


def test_actualizar_moto_existente(client):
    creada = client.post("/motos", json=moto_valida()).json()
    datos_actualizados = {**moto_valida(), "modelo": "CB650R"}

    respuesta = client.put(f"/motos/{creada['id']}", json=datos_actualizados)

    assert respuesta.status_code == 200
    assert respuesta.json()["modelo"] == "CB650R"


def test_actualizar_moto_inexistente_retorna_404(client):
    respuesta = client.put(
        "/motos/00000000-0000-0000-0000-000000000000",
        json=moto_valida(),
    )

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Moto no encontrada"}


def test_eliminar_moto_existente(client):
    creada = client.post("/motos", json=moto_valida()).json()

    respuesta = client.delete(f"/motos/{creada['id']}")

    assert respuesta.status_code == 204
    assert respuesta.content == b""
    assert client.get(f"/motos/{creada['id']}").status_code == 404


def test_eliminar_moto_inexistente_retorna_404(client):
    respuesta = client.delete("/motos/00000000-0000-0000-0000-000000000000")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Moto no encontrada"}

# =====================================================
# 1. PRUEBAS PARA GET (LISTAR)
# =====================================================

def test_get_motos_exitoso(client):
    response = client.get("/motos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_moto_inexistente(client):
    response = client.get("/motos/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

# =====================================================
# 2. PRUEBAS PARA POST (CREAR)
# =====================================================

def test_crear_moto_exitoso(client):
    payload = {
        "marca": "Honda",
        "modelo": "CB500F",
        "cilindraje": 471,
        "anio": 2024,
    }
    response = client.post("/motos", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["marca"] == "Honda"
    assert "id" in data


def test_crear_moto_datos_invalidos(client):
    payload = {
        "marca": "X",
        "modelo": "Y",
        "cilindraje": 0,
        "anio": 1800,
    }
    response = client.post("/motos", json=payload)
    assert response.status_code == 422

# =====================================================
# 3. PRUEBAS PARA GET POR ID
# =====================================================

def test_get_moto_por_id_exitoso(client):
    payload = {
        "marca": "Yamaha",
        "modelo": "MT-07",
        "cilindraje": 689,
        "anio": 2024,
    }
    create = client.post("/motos", json=payload)
    moto_id = create.json()["id"]

    response = client.get(f"/motos/{moto_id}")
    assert response.status_code == 200
    assert response.json()["id"] == moto_id


def test_get_moto_por_id_inexistente(client):
    response = client.get("/motos/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

# =====================================================
# 4. PRUEBAS PARA PUT (ACTUALIZAR)
# =====================================================

def test_actualizar_moto_exitoso(client):
    payload = {
        "marca": "Suzuki",
        "modelo": "GSX-R750",
        "cilindraje": 750,
        "anio": 2023,
    }
    create = client.post("/motos", json=payload)
    moto_id = create.json()["id"]

    update_payload = {
        "marca": "Suzuki",
        "modelo": "GSX-R1000",
        "cilindraje": 1000,
        "anio": 2024,
    }

    response = client.put(f"/motos/{moto_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["modelo"] == "GSX-R1000"


def test_actualizar_moto_inexistente(client):
    payload = {
        "marca": "No existe",
        "modelo": "X",
        "cilindraje": 200,
        "anio": 2024,
    }
    response = client.put(
        "/motos/00000000-0000-0000-0000-000000000000",
        json=payload,
    )
    assert response.status_code == 404

# =====================================================
# 5. PRUEBAS PARA DELETE (ELIMINAR)
# =====================================================

def test_eliminar_moto_exitoso(client):
    payload = {
        "marca": "Kawasaki",
        "modelo": "Ninja ZX-6R",
        "cilindraje": 636,
        "anio": 2024,
    }
    create = client.post("/motos", json=payload)
    moto_id = create.json()["id"]

    response = client.delete(f"/motos/{moto_id}")
    assert response.status_code in [200, 204]


def test_eliminar_moto_inexistente(client):
    response = client.delete("/motos/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


