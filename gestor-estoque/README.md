# API - Gestor de Estoque

Projeto desenvolvido para a atividade **CP1** da disciplina **Python (API + CRUD)** — Prof. Dr. Kévin Allan Sales Rodrigues.

**Tema escolhido:** Gestor de Estoque — controle de produtos, entradas/saídas e alertas de nível mínimo.

## Integrantes

- Nome Completo 1 — RM: 000000
- Nome Completo 2 — RM: 000000
- Nome Completo 3 — RM: 000000

> ⚠️ Substituir pelos nomes reais e RMs de todos os integrantes do grupo antes da entrega.

## Metodologia Ágil

Organização das tarefas via **Trello/Notion**: `[colar aqui o link do board]`

## Descrição do Projeto

API REST para controle de estoque, permitindo:

- Cadastro de categorias e produtos.
- Registro de movimentações de entrada e saída, com atualização automática do saldo do produto.
- Consulta de produtos que estão em ou abaixo do estoque mínimo (alerta de reposição).

## Tecnologias Utilizadas

| Tecnologia | Papel |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web para expor a API REST |
| [Uvicorn](https://www.uvicorn.org/) | Servidor ASGI |
| [SQLModel](https://sqlmodel.tiangolo.com/) | ORM (validação + mapeamento de tabelas) |
| PostgreSQL ([Neon Tech](https://neon.com)) | Banco de dados relacional na nuvem |
| python-dotenv | Carregamento de variáveis de ambiente |

## Modelagem do Banco de Dados

```
Categoria (1) ----< (N) Produto (1) ----< (N) Movimentacao
```

- **Categoria**: `id`, `nome`
- **Produto**: `id`, `nome`, `sku`, `quantidade_atual`, `estoque_minimo`, `categoria_id`
- **Movimentacao**: `id`, `produto_id`, `tipo` (`entrada`/`saida`), `quantidade`, `data`, `motivo`

## Regras de Negócio

| # | Regra | Validação/Retorno |
|---|---|---|
| 1 | Não é permitido cadastrar produto com SKU já existente | `400 Bad Request` |
| 2 | Não é permitido vincular produto a uma categoria inexistente | `400 Bad Request` |
| 3 | Não é permitido registrar movimentação com quantidade ≤ 0 | `400 Bad Request` |
| 4 | Não é permitido registrar movimentação para produto inexistente | `404 Not Found` |
| 5 | Não é permitido registrar saída maior que o saldo disponível do produto | `400 Bad Request` |
| 6 | Toda entrada soma ao `quantidade_atual`; toda saída subtrai | — |
| 7 | Um produto entra em alerta quando `quantidade_atual <= estoque_minimo` | Endpoint `GET /produtos/alertas` |
| 8 | Não é permitido excluir categoria com produtos vinculados | `400 Bad Request` |
| 9 | Não é permitido cadastrar categoria com nome já existente | `400 Bad Request` |

## Endpoints

### Categorias
| Método | Rota | Descrição |
|---|---|---|
| POST | `/categorias/` | Cria uma categoria |
| GET | `/categorias/` | Lista todas as categorias |
| GET | `/categorias/{id}` | Detalha uma categoria |
| DELETE | `/categorias/{id}` | Remove uma categoria (se sem produtos vinculados) |

### Produtos
| Método | Rota | Descrição |
|---|---|---|
| POST | `/produtos/` | Cadastra um produto |
| GET | `/produtos/` | Lista todos os produtos |
| GET | `/produtos/alertas` | Lista produtos em alerta de estoque mínimo |
| GET | `/produtos/{id}` | Detalha um produto |
| PUT | `/produtos/{id}` | Atualiza um produto |
| DELETE | `/produtos/{id}` | Remove um produto |

### Movimentações
| Método | Rota | Descrição |
|---|---|---|
| POST | `/movimentacoes/` | Registra entrada ou saída (atualiza o saldo do produto) |
| GET | `/movimentacoes/` | Lista todas as movimentações |
| GET | `/movimentacoes/produto/{produto_id}` | Histórico de movimentações de um produto |

A documentação interativa completa (Swagger) fica disponível em **`/docs`** após rodar a aplicação.

## Como Rodar o Projeto

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd gestor-estoque
```

### 2. Criar e ativar o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar a variável de ambiente
Copie o arquivo de exemplo e preencha com a sua connection string do Neon Tech:
```bash
cp .env.example .env
```
Edite o `.env`:
```
DATABASE_URL=postgresql://usuario:senha@ep-exemplo.us-east-2.aws.neon.tech/estoque_db?sslmode=require
```

> Caso o `.env` não seja configurado, a aplicação usa automaticamente um banco SQLite local (`estoque.db`) para fins de teste.

### 5. Rodar a aplicação
```bash
uvicorn app.main:app --reload
```

### 6. Acessar a documentação interativa
Abrir no navegador: **http://127.0.0.1:8000/docs**

## Estrutura do Projeto

```
gestor-estoque/
├── app/
│   ├── main.py              # instância FastAPI, startup, routers
│   ├── database.py          # engine e sessão do banco
│   ├── models.py            # modelos SQLModel (tabelas)
│   └── routers/
│       ├── categorias.py
│       ├── produtos.py
│       └── movimentacoes.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Testando a API

Todos os endpoints podem ser testados diretamente pela interface do Swagger (`/docs`), sem necessidade de ferramentas externas. Também é possível usar Postman ou Insomnia apontando para `http://127.0.0.1:8000`.
