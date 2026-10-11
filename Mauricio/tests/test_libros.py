from sqlalchemy.exc import OperationalError

from main import app
from src.database.database import get_db


def test_listar_libros_ok(client, libro_creado):
    respuesta = client.get("/libros")

    assert respuesta.status_code == 200
    assert respuesta.json() == [libro_creado]


def test_listar_libros_error_base_de_datos(client):
    def bd_caida():
        raise OperationalError("SELECT", {}, Exception("conexion rechazada"))

    app.dependency_overrides[get_db] = bd_caida

    respuesta = client.get("/libros")

    assert respuesta.status_code == 500
    assert respuesta.json() == {"detail": "Error interno de la base de datos"}


def test_obtener_libro_por_id_ok(client, libro_creado):
    respuesta = client.get(f"/libros/{libro_creado['id']}")

    assert respuesta.status_code == 200
    assert respuesta.json()["titulo"] == "Cien anos de soledad"
    assert respuesta.json()["autor"] == "Gabriel Garcia Marquez"


def test_obtener_libro_inexistente(client):
    respuesta = client.get("/libros/999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Libro no encontrado"}


def test_crear_libro_ok(client):
    nuevo = {
        "titulo": "La voragine",
        "autor": "Jose Eustasio Rivera",
        "anio": 1924,
        "disponible": False,
    }

    respuesta = client.post("/libros", json=nuevo)

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["id"] > 0
    assert datos["titulo"] == nuevo["titulo"]
    assert datos["autor"] == nuevo["autor"]
    assert datos["anio"] == nuevo["anio"]
    assert datos["disponible"] is False


def test_crear_libro_sin_titulo(client):
    respuesta = client.post(
        "/libros",
        json={"autor": "Jorge Isaacs", "anio": 1867},
    )

    assert respuesta.status_code == 422
    errores = respuesta.json()["detail"]
    assert errores[0]["loc"] == ["body", "titulo"]
    assert errores[0]["type"] == "missing"


def test_actualizar_libro_ok(client, libro_creado):
    cambios = {
        "titulo": "Cien anos de soledad (edicion especial)",
        "autor": "Gabriel Garcia Marquez",
        "anio": 2017,
        "disponible": False,
    }

    respuesta = client.put(f"/libros/{libro_creado['id']}", json=cambios)

    assert respuesta.status_code == 200
    assert respuesta.json() == {"id": libro_creado["id"], **cambios}


def test_actualizar_libro_anio_invalido(client, libro_creado):
    respuesta = client.put(
        f"/libros/{libro_creado['id']}",
        json={
            "titulo": "Cien anos de soledad",
            "autor": "Gabriel Garcia Marquez",
            "anio": "mil novecientos",
            "disponible": True,
        },
    )

    assert respuesta.status_code == 422
    errores = respuesta.json()["detail"]
    assert errores[0]["loc"] == ["body", "anio"]
    assert errores[0]["type"] == "int_parsing"


def test_eliminar_libro_ok(client, libro_creado):
    respuesta = client.delete(f"/libros/{libro_creado['id']}")

    assert respuesta.status_code == 204
    assert respuesta.content == b""
    assert client.get(f"/libros/{libro_creado['id']}").status_code == 404


def test_eliminar_libro_inexistente(client):
    respuesta = client.delete("/libros/999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"detail": "Libro no encontrado"}
