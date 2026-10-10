from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.videojuegos import Videojuego
from src.schemas.videojuegos import VideojuegoCreate, VideojuegoUpdate


def listar(db: Session) -> list[Videojuego]:
    consulta = select(Videojuego).order_by(Videojuego.titulo)
    return list(db.scalars(consulta))


def obtener_por_id(
    db: Session,
    videojuego_id: UUID,
) -> Videojuego | None:
    return db.get(Videojuego, videojuego_id)


def crear(
    db: Session,
    datos: VideojuegoCreate,
) -> Videojuego:
    videojuego = Videojuego(
        titulo=datos.titulo,
        plataforma=datos.plataforma,
        genero=datos.genero,
        precio=datos.precio,
    )

    db.add(videojuego)
    db.commit()
    db.refresh(videojuego)

    return videojuego


def actualizar(
    db: Session,
    videojuego: Videojuego,
    datos: VideojuegoUpdate,
) -> Videojuego:
    videojuego.titulo = datos.titulo
    videojuego.plataforma = datos.plataforma
    videojuego.genero = datos.genero
    videojuego.precio = datos.precio

    db.commit()
    db.refresh(videojuego)

    return videojuego


def eliminar(
    db: Session,
    videojuego: Videojuego,
) -> None:
    db.delete(videojuego)
    db.commit()
