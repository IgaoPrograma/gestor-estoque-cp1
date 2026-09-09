"""
Ponto de entrada da aplicacao FastAPI.

Responsavel por:
- instanciar o app com titulo/descricao/versao (aparecem no Swagger)
- criar as tabelas no banco na inicializacao (evento 'startup')
- registrar os routers de cada entidade (Categorias, Produtos, Movimentacoes)
"""

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routers import categorias, produtos, movimentacoes

app = FastAPI(
    title="API - Gestor de Estoque",
    description=(
        "Sistema de controle de produtos, entradas/saidas e alertas de "
        "nivel minimo de estoque. Projeto desenvolvido para a atividade "
        "CP1 da disciplina Python (API + CRUD)."
    ),
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    """Cria as tabelas no banco de dados (caso ainda nao existam) ao subir a aplicacao."""
    SQLModel.metadata.create_all(engine)


app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(movimentacoes.router)


@app.get("/", tags=["Status"])
def raiz():
    """Endpoint simples para verificar se a API esta no ar."""
    return {"status": "online", "mensagem": "API Gestor de Estoque no ar. Acesse /docs para a documentacao interativa."}
