from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base


class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    autor: Mapped[str] = mapped_column(String(120), nullable=False)
    anio: Mapped[int] = mapped_column(nullable=False)
    disponible: Mapped[bool] = mapped_column(default=True, nullable=False)
