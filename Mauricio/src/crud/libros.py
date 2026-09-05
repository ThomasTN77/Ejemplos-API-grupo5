from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.libros import Libro
from src.schemas.libros import LibroCreate, LibroUpdate


def listar(db: Session) -> list[Libro]:
    consulta = select(Libro).order_by(Libro.titulo)
    return list(db.scalars(consulta))


def obtener_por_id(db: Session, libro_id: int) -> Libro | None:
    return db.get(Libro, libro_id)


def crear(db: Session, datos: LibroCreate) -> Libro:
    libro = Libro(
        titulo=datos.titulo,
        autor=datos.autor,
        anio=datos.anio,
        disponible=datos.disponible,
    )

    db.add(libro)
    db.commit()
    db.refresh(libro)

    return libro


def actualizar(db: Session, libro: Libro, datos: LibroUpdate) -> Libro:
    libro.titulo = datos.titulo
    libro.autor = datos.autor
    libro.anio = datos.anio
    libro.disponible = datos.disponible

    db.commit()
    db.refresh(libro)

    return libro


def eliminar(db: Session, libro: Libro) -> None:
    db.delete(libro)
    db.commit()
