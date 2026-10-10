from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import videojuegos as repo
from src.database.database import get_db
from src.schemas.videojuegos import VideojuegoCreate, VideojuegoRead, VideojuegoUpdate


router = APIRouter(
    prefix="/videojuegos",
    tags=["videojuegos"],
)


@router.get("", response_model=list[VideojuegoRead])
def listar_videojuegos(db: Session = Depends(get_db)):
    return repo.listar(db)


@router.get("/{videojuego_id}", response_model=VideojuegoRead)
def obtener_videojuego(
    videojuego_id: UUID,
    db: Session = Depends(get_db),
):
    videojuego = repo.obtener_por_id(db, videojuego_id)

    if videojuego is None:
        raise HTTPException(
            status_code=404,
            detail="Videojuego no encontrado",
        )

    return videojuego


@router.post(
    "",
    response_model=VideojuegoRead,
    status_code=status.HTTP_201_CREATED,
)
def crear_videojuego(
    datos: VideojuegoCreate,
    db: Session = Depends(get_db),
):
    return repo.crear(db, datos)


@router.put(
    "/{videojuego_id}",
    response_model=VideojuegoRead,
)
def actualizar_videojuego(
    videojuego_id: UUID,
    datos: VideojuegoUpdate,
    db: Session = Depends(get_db),
):
    videojuego = repo.obtener_por_id(db, videojuego_id)

    if videojuego is None:
        raise HTTPException(
            status_code=404,
            detail="Videojuego no encontrado",
        )

    return repo.actualizar(db, videojuego, datos)


@router.delete(
    "/{videojuego_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_videojuego(
    videojuego_id: UUID,
    db: Session = Depends(get_db),
):
    videojuego = repo.obtener_por_id(db, videojuego_id)

    if videojuego is None:
        raise HTTPException(
            status_code=404,
            detail="Videojuego no encontrado",
        )

    repo.eliminar(db, videojuego)
