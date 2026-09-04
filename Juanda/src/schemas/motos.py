from uuid import UUID

from pydantic import BaseModel, Field


class MotoCreate(BaseModel):
    marca: str = Field(min_length=1, max_length=80)
    modelo: str = Field(min_length=1, max_length=120)
    cilindraje: int = Field(ge=1, le=3000)
    anio: int = Field(ge=1900, le=2100)


class MotoUpdate(BaseModel):
    marca: str = Field(min_length=1, max_length=80)
    modelo: str = Field(min_length=1, max_length=120)
    cilindraje: int = Field(ge=1, le=3000)
    anio: int = Field(ge=1900, le=2100)


class MotoRead(BaseModel):
    id: UUID
    marca: str
    modelo: str
    cilindraje: int
    anio: int

    model_config = {
        "from_attributes": True,
    }
