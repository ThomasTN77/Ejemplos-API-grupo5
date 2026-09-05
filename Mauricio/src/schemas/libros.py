from pydantic import BaseModel, Field


class LibroBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    autor: str = Field(min_length=1, max_length=120)
    anio: int = Field(ge=1400, le=2100)
    disponible: bool = True


class LibroCreate(LibroBase):
    """Datos que llegan en el POST."""


class LibroUpdate(LibroBase):
    """Datos que llegan en el PUT."""


class LibroRead(LibroBase):
    """Datos que devuelve la API."""

    id: int

    model_config = {"from_attributes": True}
