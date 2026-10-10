from uuid import UUID

from sqlalchemy import select 


from src.database.database import SessionLocal
from src.entities.motos import Moto


SEED_MOTOS = (
    {
        "id": UUID("11111111-1111-1111-1111-111111111111"),
        "marca": "Honda",
        "modelo": "CB500F",
        "cilindraje": 471,
        "anio": 2024,
    },
    {
        "id": UUID("22222222-2222-2222-2222-222222222222"),
        "marca": "Yamaha",
        "modelo": "MT-07",
        "cilindraje": 689,
        "anio": 2024,
    },
)


def seed() -> None:
    with SessionLocal() as db:
        for moto_data in SEED_MOTOS:
            exists = db.scalar(select(Moto.id).where(Moto.id == moto_data["id"]))
            if exists is None:
                db.add(Moto(**moto_data))
        db.commit()


if __name__ == "__main__":
    seed()