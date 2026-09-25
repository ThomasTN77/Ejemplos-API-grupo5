from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class MotoBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    marca: str = Field(min_length=1, max_length=80)
    modelo: str = Field(min_length=1, max_length=120)
    cilindraje: int = Field(ge=1, le=3000)
    anio: int = Field(ge=1900, le=2100)

    @field_validator("marca", "modelo")
    @classmethod
    def validar_texto_no_vacio(cls, valor: str) -> str:
        if not valor:
            raise ValueError("no puede estar vacio")
        return valor


class MotoCreate(MotoBase):
    pass


class MotoUpdate(MotoBase):
    pass


class MotoRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    marca: str
    modelo: str
    cilindraje: int
    anio: int
