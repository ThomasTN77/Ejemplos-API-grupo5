from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.crud import libros as repo
from src.database.database import get_db
from src.schemas.libros import LibroCreate, LibroRead, LibroUpdate

router = APIRouter(prefix="/libros", tags=["libros"])


def _buscar_o_404(db: Session, libro_id: int):
    libro = repo.obtener_por_id(db, libro_id)

    if libro is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return libro


@router.get("", response_model=list[LibroRead])
def listar_libros(db: Session = Depends(get_db)):
    return repo.listar(db)


@router.get("/{libro_id}", response_model=LibroRead)
def obtener_libro(libro_id: int, db: Session = Depends(get_db)):
    return _buscar_o_404(db, libro_id)


@router.post("", response_model=LibroRead, status_code=status.HTTP_201_CREATED)
def crear_libro(datos: LibroCreate, db: Session = Depends(get_db)):
    return repo.crear(db, datos)


@router.put("/{libro_id}", response_model=LibroRead)
def actualizar_libro(
    libro_id: int,
    datos: LibroUpdate,
    db: Session = Depends(get_db),
):
    libro = _buscar_o_404(db, libro_id)
    return repo.actualizar(db, libro, datos)


@router.delete("/{libro_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = _buscar_o_404(db, libro_id)
    repo.eliminar(db, libro)
