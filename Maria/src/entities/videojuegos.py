from uuid import UUID, uuid4

from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Videojuego(Base):
    __tablename__ = "videojuegos"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
    )
    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    plataforma: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    genero: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )
    precio: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
