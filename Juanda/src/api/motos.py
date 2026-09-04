from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import motos as repo
from src.database.database import get_db
from src.schemas.motos import MotoCreate, MotoRead, MotoUpdate


router = APIRouter(
    prefix="/motos",
    tags=["motos"],
)


@router.get("", response_model=list[MotoRead])
def listar_motos(db: Session = Depends(get_db)):
    return repo.listar(db)


@router.get("/{moto_id}", response_model=MotoRead)
def obtener_moto(
    moto_id: UUID,
    db: Session = Depends(get_db),
):
    moto = repo.obtener_por_id(db, moto_id)

    if moto is None:
        raise HTTPException(
            status_code=404,
            detail="Moto no encontrada",
        )

    return moto


@router.post(
    "",
    response_model=MotoRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_moto(
    datos: MotoCreate,
    db: Session = Depends(get_db),
):
    return repo.crear(db, datos)


@router.put(
    "/{moto_id}",
    response_model=MotoRead,
)
def actualizar_moto(
    moto_id: UUID,
    datos: MotoUpdate,
    db: Session = Depends(get_db),
):
    moto = repo.obtener_por_id(db, moto_id)

    if moto is None:
        raise HTTPException(
            status_code=404,
            detail="Moto no encontrada",
        )

    return repo.actualizar(db, moto, datos)


@router.delete(
    "/{moto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_moto(
    moto_id: UUID,
    db: Session = Depends(get_db),
):
    moto = repo.obtener_por_id(db, moto_id)

    if moto is None:
        raise HTTPException(
            status_code=404,
            detail="Moto no encontrada",
        )

    repo.eliminar(db, moto)
