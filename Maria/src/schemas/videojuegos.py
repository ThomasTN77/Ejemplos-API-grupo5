from uuid import UUID

from pydantic import BaseModel, Field


class VideojuegoCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    plataforma: str = Field(min_length=1, max_length=120)
    genero: str = Field(min_length=1, max_length=120)
    precio: float = Field(ge=0)


class VideojuegoUpdate(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    plataforma: str = Field(min_length=1, max_length=120)
    genero: str = Field(min_length=1, max_length=120)
    precio: float = Field(ge=0)


class VideojuegoRead(BaseModel):
    id: UUID
    titulo: str
    plataforma: str
    genero: str
    precio: float

    model_config = {
        "from_attributes": True,
    }
