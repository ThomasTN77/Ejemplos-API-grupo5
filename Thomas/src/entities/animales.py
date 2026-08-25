from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Animal(Base):
    __tablename__ = "animales"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    nombre: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    especie: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    edad: Mapped[int] = mapped_column(nullable=False)
