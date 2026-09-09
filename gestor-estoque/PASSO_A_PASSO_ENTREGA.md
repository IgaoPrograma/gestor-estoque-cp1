# Passo a Passo para Concluir e Entregar a CP1 (Gestor de Estoque)

Todo o código já está pronto e testado. Siga os passos abaixo na ordem — não é necessário escrever nenhuma linha de código, apenas configurar e executar.

---

## Parte 1 — Banco de dados no Neon Tech (~15 min)

1. Acesse **https://neon.com** e crie sua conta (pode usar login com Gmail).
2. Crie uma **organização** (qualquer nome) e selecione o plano **Free**.
3. Clique em **Create project**, dê um nome (ex.: `gestor-estoque`), escolha a região e a versão do PostgreSQL (pode deixar as opções padrão).
4. Dentro do projeto, vá em **Databases** → **Add database** → dê um nome, por exemplo `estoque_db` → **Create**.
5. Volte para a tela principal do projeto e clique em **Connect**.
6. Selecione o database criado (`estoque_db`) e copie a **connection string** — algo como:
   ```
   postgresql://neondb_owner:SENHA@ep-xxxxx.us-east-2.aws.neon.tech/estoque_db?sslmode=require
   ```
   Guarde essa string, você vai usá-la no Passo 2.5.

---

## Parte 2 — Preparar o ambiente local (~15 min)

1. Extraia a pasta `gestor-estoque` que você recebeu em um local de fácil acesso no seu computador.
2. Abra um terminal (ou o VS Code) dentro dessa pasta.
3. Crie o ambiente virtual:
   ```bash
   python -m venv venv
   ```
4. Ative o ambiente virtual:
   - **Windows:** `venv\Scripts\activate`
   - **Mac/Linux:** `source venv/bin/activate`
5. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
6. Copie o arquivo de exemplo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```
   (no Windows, pode simplesmente duplicar o arquivo `.env.example` e renomear para `.env`)
7. Abra o arquivo `.env` em um editor de texto e cole a connection string que você copiou do Neon Tech no lugar do valor de exemplo:
   ```
   DATABASE_URL=postgresql://neondb_owner:SUA_SENHA@ep-xxxxx.us-east-2.aws.neon.tech/estoque_db?sslmode=require
   ```
   Salve o arquivo.

---

## Parte 3 — Rodar e testar a API (~20 min)

1. Ainda no terminal (com o ambiente virtual ativado), rode:
   ```bash
   uvicorn app.main:app --reload
   ```
2. Você deve ver uma mensagem como `Uvicorn running on http://127.0.0.1:8000`.
3. Abra o navegador em **http://127.0.0.1:8000/docs** — essa é a documentação interativa (Swagger) gerada automaticamente.
4. Teste a aplicação na seguinte ordem (clique em cada endpoint, depois em "Try it out" e "Execute"):
   1. `POST /categorias/` → crie uma categoria, ex.: `{"nome": "Eletronicos"}`.
   2. `POST /produtos/` → crie um produto vinculado à categoria criada, ex.:
      ```json
      {"nome": "Mouse", "sku": "MOU-001", "quantidade_atual": 10, "estoque_minimo": 5, "categoria_id": 1}
      ```
   3. `POST /movimentacoes/` → registre uma saída, ex.:
      ```json
      {"produto_id": 1, "tipo": "saida", "quantidade": 3, "motivo": "venda"}
      ```
   4. `GET /produtos/{id}` → confirme que o saldo do produto foi atualizado (deve estar em 7).
   5. `GET /produtos/alertas` → registre mais saídas até o saldo ficar igual ou abaixo de 5, e veja o produto aparecer na lista de alerta.
   6. Teste também os casos de erro: tente criar um produto com SKU repetido, ou uma saída maior que o saldo disponível — a API deve responder com erro `400`.
5. Se tudo funcionar como esperado, a API está validada. Pare o servidor com `Ctrl + C`.

---

## Parte 4 — Subir para o GitHub (~10 min)

1. Crie um repositório novo no GitHub (ex.: `gestor-estoque-cp1`), público ou privado com acesso liberado ao professor.
2. No terminal, dentro da pasta do projeto:
   ```bash
   git init
   git add .
   git commit -m "CP1 - Gestor de Estoque"
   git branch -M main
   git remote add origin <URL-DO-SEU-REPOSITORIO>
   git push -u origin main
   ```
3. Confirme no GitHub que o arquivo `.env` **não** foi enviado (ele deve ser ignorado automaticamente pelo `.gitignore`). Se ele aparecer no repositório, remova-o imediatamente e troque a senha do banco no Neon Tech por segurança.

---

## Parte 5 — Finalizar o README e a entrega (~15 min)

1. Abra o arquivo `README.md` e substitua a seção **Integrantes** pelos nomes reais e RMs do grupo.
2. Cole o link do board do Trello ou Notion na seção **Metodologia Ágil**.
3. Faça o commit final dessa alteração:
   ```bash
   git add README.md
   git commit -m "Atualiza README com integrantes e link do board"
   git push
   ```
4. Crie (ou finalize) o board no Trello/Notion com pelo menos as colunas `A Fazer / Em Progresso / Concluído` e os cartões referentes às etapas deste documento marcados como concluídos.
5. Entregue conforme solicitado pelo professor: link do repositório GitHub + link do board.

---

## Checklist Final Antes de Entregar

- [ ] Conta e projeto criados no Neon Tech, com a `DATABASE_URL` funcionando.
- [ ] Projeto rodando localmente sem erros (`uvicorn app.main:app --reload`).
- [ ] Todos os endpoints testados no Swagger (`/docs`), incluindo os casos de erro (400/404).
- [ ] Regras de negócio validadas na prática (saldo insuficiente, alerta de estoque mínimo, SKU duplicado, categoria com produtos vinculados).
- [ ] `.env` **não** commitado no GitHub.
- [ ] README com nomes de todos os integrantes e tema indicado.
- [ ] Regras de negócio documentadas no README.
- [ ] Board Trello/Notion criado e atualizado.
- [ ] Repositório GitHub público (ou com acesso liberado ao professor).

Se todos os itens acima estiverem marcados, a entrega atende a 100% dos critérios do enunciado da CP1.
