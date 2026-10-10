from sqlalchemy import select

from src.database.database import SessionLocal
from src.entities.libros import Libro

LIBROS = [
    {"titulo": "Cien anos de soledad", "autor": "Gabriel Garcia Marquez", "anio": 1967},
    {"titulo": "La voragine", "autor": "Jose Eustasio Rivera", "anio": 1924},
    {"titulo": "Maria", "autor": "Jorge Isaacs", "anio": 1867},
    {"titulo": "Rosario Tijeras", "autor": "Jorge Franco", "anio": 1999},
    {"titulo": "El olvido que seremos", "autor": "Hector Abad Faciolince", "anio": 2006},
]


def ejecutar_seeder():
    db = SessionLocal()
    insertados = 0

    try:
        for datos in LIBROS:
            existe = db.scalar(select(Libro).where(Libro.titulo == datos["titulo"]))

            if existe is None:
                db.add(Libro(**datos))
                insertados += 1

        db.commit()
        print(f"Seeder terminado: {insertados} libros insertados.")
    finally:
        db.close()


if __name__ == "__main__":
    ejecutar_seeder()
