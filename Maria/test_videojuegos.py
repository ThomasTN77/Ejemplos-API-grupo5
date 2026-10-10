import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ==========================================
# 1. PRUEBAS PARA GET (LISTAR)
# ==========================================
def test_get_videojuegos_exitoso():
    response = client.get("/videojuegos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_videojuegos_ruta_invalida():
    response = client.get("/videojuegos_inexistente/")
    assert response.status_code == 404


# ==========================================
# 2. PRUEBAS PARA POST (CREAR)
# ==========================================
def test_crear_videojuego_exitoso():
    payload = {
        "titulo": "Game Test Pytest",
        "plataforma": "PC",
        "genero": "Aventura",
        "precio": 29.99
    }
    response = client.post("/videojuegos/", json=payload)
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["titulo"] == "Game Test Pytest"
    assert "id" in data

def test_crear_videojuego_datos_invalidos():
    payload = {
        "plataforma": "PC"
    }
    response = client.post("/videojuegos/", json=payload)
    assert response.status_code == 422


# ==========================================
# 3. PRUEBAS PARA GET POR ID (OBTENER UNO)
# ==========================================
def test_get_videojuego_por_id_exitoso():
    payload = {
        "titulo": "Test Get ID",
        "plataforma": "Console",
        "genero": "RPG",
        "precio": 49.99
    }
    create_res = client.post("/videojuegos/", json=payload)
    game_id = create_res.json()["id"]

    response = client.get(f"/videojuegos/{game_id}")
    assert response.status_code == 200
    assert response.json()["id"] == game_id

def test_get_videojuego_por_id_inexistente():
    response = client.get("/videojuegos/999999")
    assert response.status_code in [404, 422]


# ==========================================
# 4. PRUEBAS PARA PUT (ACTUALIZAR)
# ==========================================
def test_actualizar_videojuego_exitoso():
    payload = {
        "titulo": "Update Normal",
        "plataforma": "PC",
        "genero": "Accion",
        "precio": 10.00
    }
    create_res = client.post("/videojuegos/", json=payload)
    game_id = create_res.json()["id"]

    update_payload = {
        "titulo": "Update Exitoso Editado",
        "plataforma": "PC",
        "genero": "Accion",
        "precio": 15.00
    }
    response = client.put(f"/videojuegos/{game_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["titulo"] == "Update Exitoso Editado"

def test_actualizar_videojuego_id_inexistente():
    update_payload = {
        "titulo": "No existe",
        "plataforma": "PC",
        "genero": "Accion",
        "precio": 15.00
    }
    response = client.put("/videojuegos/999999", json=update_payload)
    assert response.status_code in [404, 422]


# ==========================================
# 5. PRUEBAS PARA DELETE (ELIMINAR)
# ==========================================
def test_eliminar_videojuego_exitoso():
    payload = {
        "titulo": "Para borrar",
        "plataforma": "PC",
        "genero": "Arcade",
        "precio": 5.00
    }
    create_res = client.post("/videojuegos/", json=payload)
    game_id = create_res.json()["id"]

    response = client.delete(f"/videojuegos/{game_id}")
    assert response.status_code in [200, 204]

def test_eliminar_videojuego_id_inexistente():
    response = client.delete("/videojuegos/999999")
    assert response.status_code in [404, 422]