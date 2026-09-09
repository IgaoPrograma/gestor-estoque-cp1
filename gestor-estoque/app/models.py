"""
Modelos de dados (tabelas) da aplicacao, definidos com SQLModel.

SQLModel une, na mesma classe:
- validacao de dados (como o Pydantic faz)
- mapeamento para uma tabela do banco relacional (como o SQLAlchemy faz)

Entidades do dominio "Gestor de Estoque":
- Categoria: agrupa produtos (ex.: "Eletronicos", "Limpeza")
- Produto: item do estoque, com quantidade atual e estoque minimo
- Movimentacao: historico de entradas e saidas de um produto
"""

from typing import Optional, List
from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel, Relationship


class TipoMovimentacao(str, Enum):
    """Tipo de movimentacao de estoque: entrada (compra/recebimento) ou saida (venda/consumo)."""
    ENTRADA = "entrada"
    SAIDA = "saida"


class Categoria(SQLModel, table=True):
    """Categoria de produtos (ex.: Eletronicos, Limpeza, Alimentos)."""

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True, unique=True)

    produtos: List["Produto"] = Relationship(back_populates="categoria")


class Produto(SQLModel, table=True):
    """
    Produto controlado no estoque.

    quantidade_atual: saldo disponivel agora (atualizado a cada movimentacao)
    estoque_minimo: limite abaixo do qual o produto entra em alerta de reposicao
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    sku: str = Field(index=True, unique=True)
    quantidade_atual: int = Field(default=0, ge=0)
    estoque_minimo: int = Field(default=0, ge=0)
    categoria_id: Optional[int] = Field(default=None, foreign_key="categoria.id")

    categoria: Optional[Categoria] = Relationship(back_populates="produtos")
    movimentacoes: List["Movimentacao"] = Relationship(back_populates="produto")


class Movimentacao(SQLModel, table=True):
    """Registro de uma entrada ou saida de um produto no estoque."""

    id: Optional[int] = Field(default=None, primary_key=True)
    produto_id: int = Field(foreign_key="produto.id")
    tipo: TipoMovimentacao
    quantidade: int
    data: datetime = Field(default_factory=datetime.utcnow)
    motivo: Optional[str] = None

    produto: Optional[Produto] = Relationship(back_populates="movimentacoes")
