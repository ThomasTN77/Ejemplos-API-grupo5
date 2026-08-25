from uuid import UUID

from pydantic import BaseModel, Field


class AnimalCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    especie: str = Field(min_length=1, max_length=120)
    edad: int = Field(ge=0, le=200)


class AnimalUpdate(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    especie: str = Field(min_length=1, max_length=120)
    edad: int = Field(ge=0, le=200)


class AnimalRead(BaseModel):
    id: UUID
    nombre: str
    especie: str
    edad: int

    model_config = {
        "from_attributes": True,
    }
