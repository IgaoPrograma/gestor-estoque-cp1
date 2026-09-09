"""
Endpoints de Produto.

Regras de negocio aplicadas aqui:
- Nao e permitido cadastrar produto com SKU duplicado.
- Nao e permitido vincular um produto a uma categoria inexistente.
- Endpoint /produtos/alertas retorna os produtos cujo saldo atual esta
  igual ou abaixo do estoque minimo definido (o alerta de reposicao
  central do tema "Gestor de Estoque").

Atencao a ordem das rotas: '/produtos/alertas' precisa ser declarada
ANTES de '/produtos/{produto_id}', senao o FastAPI tentaria interpretar
'alertas' como se fosse um ID de produto.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session
from app.models import Produto, Categoria

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("/", response_model=Produto, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: Produto, session: Session = Depends(get_session)):
    """Cadastra um novo produto no estoque."""
    if produto.categoria_id is not None:
        categoria = session.get(Categoria, produto.categoria_id)
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoria com ID {produto.categoria_id} nao encontrada.",
            )

    existente = session.exec(select(Produto).where(Produto.sku == produto.sku)).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ja existe um produto com o SKU '{produto.sku}'.",
        )

    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto


@router.get("/", response_model=List[Produto])
def listar_produtos(session: Session = Depends(get_session)):
    """Lista todos os produtos cadastrados."""
    return session.exec(select(Produto)).all()


@router.get("/alertas", response_model=List[Produto])
def listar_produtos_abaixo_do_minimo(session: Session = Depends(get_session)):
    """Lista os produtos cujo saldo atual esta igual ou abaixo do estoque minimo (alerta de reposicao)."""
    statement = select(Produto).where(Produto.quantidade_atual <= Produto.estoque_minimo)
    return session.exec(statement).all()


@router.get("/{produto_id}", response_model=Produto)
def detalhar_produto(produto_id: int, session: Session = Depends(get_session)):
    """Retorna os dados de um produto especifico."""
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado.")
    return produto


@router.put("/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, dados: Produto, session: Session = Depends(get_session)):
    """Atualiza os dados cadastrais de um produto (nome, sku, categoria, estoque minimo etc.)."""
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado.")

    dados_atualizados = dados.dict(exclude_unset=True, exclude={"id"})
    for campo, valor in dados_atualizados.items():
        setattr(produto, campo, valor)

    session.add(produto)
    session.commit()
    session.refresh(produto)
    return produto


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(produto_id: int, session: Session = Depends(get_session)):
    """Remove um produto do cadastro."""
    produto = session.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto nao encontrado.")
    session.delete(produto)
    session.commit()
    return None
