from uuid import UUID, uuid4

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Moto(Base):
    __tablename__ = "motos"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    marca: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    modelo: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    cilindraje: Mapped[int] = mapped_column(nullable=False)
    anio: Mapped[int] = mapped_column(nullable=False)
