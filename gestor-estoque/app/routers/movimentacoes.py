"""
Endpoints de Movimentacao (entradas e saidas de estoque).

Este e o modulo com as regras de negocio mais importantes do projeto:
1. A movimentacao so pode ser registrada se o produto existir.
2. A quantidade movimentada deve ser maior que zero.
3. Uma saida nao pode ser maior que o saldo atual disponivel do produto.
4. Toda entrada soma ao saldo do produto; toda saida subtrai.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Movimentacao, Produto, TipoMovimentacao

router = APIRouter(prefix="/movimentacoes", tags=["Movimentacoes"])


@router.post("/", response_model=Movimentacao, status_code=status.HTTP_201_CREATED)
def registrar_movimentacao(mov: Movimentacao, session: Session = Depends(get_session)):
    """Registra uma entrada ou saida de estoque e atualiza o saldo do produto."""
    produto = session.get(Produto, mov.produto_id)
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {mov.produto_id} nao encontrado.",
        )

    if mov.quantidade <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A quantidade movimentada deve ser maior que zero.",
        )

    if mov.tipo == TipoMovimentacao.SAIDA and mov.quantidade > produto.quantidade_atual:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estoque insuficiente para saida. Disponivel: {produto.quantidade_atual}.",
        )

    if mov.tipo == TipoMovimentacao.ENTRADA:
        produto.quantidade_atual += mov.quantidade
    else:
        produto.quantidade_atual -= mov.quantidade

    session.add(produto)
    session.add(mov)
    session.commit()
    session.refresh(mov)
    return mov


@router.get("/", response_model=List[Movimentacao])
def listar_movimentacoes(session: Session = Depends(get_session)):
    """Lista todas as movimentacoes registradas no sistema."""
    return session.exec(select(Movimentacao)).all()


@router.get("/produto/{produto_id}", response_model=List[Movimentacao])
def historico_por_produto(produto_id: int, session: Session = Depends(get_session)):
    """Lista o historico de movimentacoes de um produto especifico."""
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado.")

    statement = select(Movimentacao).where(Movimentacao.produto_id == produto_id)
    return session.exec(statement).all()
