"""
Endpoints de Categoria.

Regra de negocio aplicada aqui:
- Nao e permitido remover uma categoria que ainda possua produtos vinculados
  (evita deixar produtos "orfaos" ou perder a integridade dos dados).
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Categoria, Produto

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/", response_model=Categoria, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria: Categoria, session: Session = Depends(get_session)):
    """Cria uma nova categoria de produtos."""
    existente = session.exec(select(Categoria).where(Categoria.nome == categoria.nome)).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ja existe uma categoria chamada '{categoria.nome}'.",
        )
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria


@router.get("/", response_model=List[Categoria])
def listar_categorias(session: Session = Depends(get_session)):
    """Lista todas as categorias cadastradas."""
    return session.exec(select(Categoria)).all()


@router.get("/{categoria_id}", response_model=Categoria)
def detalhar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """Retorna os dados de uma categoria especifica."""
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria nao encontrada.")
    return categoria


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_categoria(categoria_id: int, session: Session = Depends(get_session)):
    """Remove uma categoria, desde que nao existam produtos vinculados a ela."""
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoria nao encontrada.")

    produtos_vinculados = session.exec(
        select(Produto).where(Produto.categoria_id == categoria_id)
    ).all()
    if produtos_vinculados:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nao e possivel remover uma categoria que possui produtos vinculados.",
        )

    session.delete(categoria)
    session.commit()
    return None
