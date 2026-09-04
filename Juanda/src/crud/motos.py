from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.motos import Moto
from src.schemas.motos import MotoCreate, MotoUpdate


def listar(db: Session) -> list[Moto]:
    consulta = select(Moto).order_by(Moto.marca, Moto.modelo)
    return list(db.scalars(consulta))


def obtener_por_id(db: Session, moto_id: UUID) -> Moto | None:
    return db.get(Moto, moto_id)


def crear(db: Session, datos: MotoCreate) -> Moto:
    moto = Moto(
        marca=datos.marca,
        modelo=datos.modelo,
        cilindraje=datos.cilindraje,
        anio=datos.anio,
    )

    db.add(moto)
    db.commit()
    db.refresh(moto)

    return moto


def actualizar(db: Session, moto: Moto, datos: MotoUpdate) -> Moto:
    moto.marca = datos.marca
    moto.modelo = datos.modelo
    moto.cilindraje = datos.cilindraje
    moto.anio = datos.anio

    db.commit()
    db.refresh(moto)

    return moto


def eliminar(db: Session, moto: Moto) -> None:
    db.delete(moto)
    db.commit()
