"""
Configuracao da conexao com o banco de dados.

A URL de conexao vem da variavel de ambiente DATABASE_URL (arquivo .env),
nunca hardcoded no codigo-fonte -- isso evita expor usuario/senha do banco
no repositorio (um dos riscos citados no material da disciplina).

Se DATABASE_URL nao estiver definida, cai para um arquivo SQLite local
(estoque.db), util para rodar/testar rapidamente sem depender do Neon Tech.
"""

import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./estoque.db")

# SQLite exige essa flag quando usado com FastAPI (varias threads acessando a mesma conexao)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def get_session():
    """
    Dependencia do FastAPI que fornece uma sessao de banco por requisicao.

    O uso de 'yield' dentro do 'with' garante que a sessao seja aberta antes
    do endpoint executar e fechada automaticamente depois, mesmo se ocorrer
    uma excecao no meio do caminho.
    """
    with Session(engine) as session:
        yield session
