
# Mentoria MVP (KNN) — Versão com Banco de Dados

## Opção 1: rodar rápido com SQLite (sem instalar MySQL)
```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt

# criar/atualizar schema e subir API
.\.venv\Scripts\python app_db.py  # cria mentoria.db

# popular com muitos mentores
.\.venv\Scripts\python seed_db.py

# abrir o frontend
start frontend.html   # Windows
```
A API estará em http://localhost:8000

## Opção 2: usar MySQL (produção)
1. Crie o banco `mentoria` no MySQL.
2. Copie `.env.example` para `.env` e edite:
```
DATABASE_URL=mysql+pymysql://usuario:senha@localhost:3306/mentoria
```
3. Instale dependências e rode:
```bash
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python app_db.py
.\.venv\Scripts\python seed_db.py
```

## Endpoints
- `GET /mentores` — lista mentores do banco
- `POST /mentores` — cadastra mentor (JSON: nome, curso, interesse, disponibilidade, instituicao)
- `POST /recomendar` — retorna mentores do **mesmo curso**, ordenados por **compatibilidade (0–10)**

## Observações
- ORM: SQLAlchemy 2.0 (compatível com SQLite e MySQL via pymysql).
- Similaridade fixa em cosseno; compatibilidade = (1 - distância)*10.
- LGPD: dados sintéticos gerados no `seed_db.py`.
