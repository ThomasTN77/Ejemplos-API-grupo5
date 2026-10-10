from uuid import UUID

from sqlalchemy import select

from src.database.database import SessionLocal
from src.entities.animales import Animal


SEED_ANIMALES = (
    {
        "id": UUID("33333333-3333-3333-3333-333333333333"),
        "nombre": "Luna",
        "especie": "Perro",
        "edad": 4,
    },
    {
        "id": UUID("44444444-4444-4444-4444-444444444444"),
        "nombre": "Michi",
        "especie": "Gato",
        "edad": 2,
    },
)


def seed() -> None:
    with SessionLocal() as db:
        for animal_data in SEED_ANIMALES:
            exists = db.scalar(
                select(Animal.id).where(Animal.id == animal_data["id"])
            )
            if exists is None:
                db.add(Animal(**animal_data))
        db.commit()


if __name__ == "__main__":
    seed()