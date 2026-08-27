from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.entities.animales import Animal
from src.schemas.animales import AnimalCreate, AnimalUpdate


def listar(db: Session) -> list[Animal]:
    consulta = select(Animal).order_by(Animal.nombre)
    return list(db.scalars(consulta))


def obtener_por_id(
    db: Session,
    animal_id: UUID,
) -> Animal | None:
    return db.get(Animal, animal_id)


def crear(
    db: Session,
    datos: AnimalCreate,
) -> Animal:
    animal = Animal(
        nombre=datos.nombre,
        especie=datos.especie,
        edad=datos.edad,
    )

    db.add(animal)
    db.commit()
    db.refresh(animal)

    return animal


def actualizar(
    db: Session,
    animal: Animal,
    datos: AnimalUpdate,
) -> Animal:
    animal.nombre = datos.nombre
    animal.especie = datos.especie
    animal.edad = datos.edad

    db.commit()
    db.refresh(animal)

    return animal


def eliminar(
    db: Session,
    animal: Animal,
) -> None:
    db.delete(animal)
    db.commit()
