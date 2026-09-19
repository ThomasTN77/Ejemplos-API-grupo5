from pydantic import BaseModel, Field


class LibroBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    autor: str = Field(min_length=1, max_length=120)
    anio: int = Field(ge=1400, le=2100)
    disponible: bool = True


class LibroCreate(LibroBase):
    pass


class LibroUpdate(LibroBase):
    pass


class LibroRead(LibroBase):
    id: int

    model_config = {"from_attributes": True}
