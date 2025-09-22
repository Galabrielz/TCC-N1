
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, Mentor
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.neighbors import NearestNeighbors

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///mentoria.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)

app = Flask(__name__)
CORS(app)

CATEGORICAL_COLS = ["curso","interesse","disponibilidade","instituicao"]

def ensure_schema():
    Base.metadata.create_all(engine)

def df_from_mentores(mentores):
    data = [{
        "id": m.id,
        "nome": m.nome,
        "curso": m.curso,
        "interesse": m.interesse,
        "disponibilidade": m.disponibilidade,
        "instituicao": m.instituicao
    } for m in mentores]
    return pd.DataFrame(data)

@app.get("/mentores")
def list_mentores():
    with Session(engine) as s:
        mentores = s.scalars(select(Mentor)).all()
        return jsonify([{
            "id": m.id, "nome": m.nome, "curso": m.curso,
            "interesse": m.interesse, "disponibilidade": m.disponibilidade,
            "instituicao": m.instituicao
        } for m in mentores])

@app.post("/mentores")
def add_mentor():
    payload = request.json or {}
    missing = [c for c in ["nome"] + CATEGORICAL_COLS if c not in payload or not payload[c]]
    if missing:
        return jsonify({"error": f"Campos obrigatórios ausentes: {', '.join(missing)}"}), 400
    with Session(engine) as s:
        m = Mentor(
            nome=payload["nome"],
            curso=payload["curso"],
            interesse=payload["interesse"],
            disponibilidade=payload["disponibilidade"],
            instituicao=payload["instituicao"]
        )
        s.add(m)
        s.commit()
        return jsonify({"ok": True, "id": m.id})

@app.post("/recomendar")
def recomendar():
    payload = request.json or {}
    query = {c: payload.get(c, "") for c in CATEGORICAL_COLS}
    if any(v == "" for v in query.values()):
        return jsonify({"error": "Informe curso, interesse, disponibilidade e instituicao"}), 400

    # filtra por curso
    with Session(engine) as s:
        mentores = s.scalars(select(Mentor).where(Mentor.curso == query["curso"])).all()
    if not mentores:
        return jsonify({"consulta": query, "recomendacoes": []})

    df = df_from_mentores(mentores)

    enc = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
    X = enc.fit_transform(df[CATEGORICAL_COLS])
    q_vec = enc.transform(pd.DataFrame([query]))

    nn = NearestNeighbors(n_neighbors=len(df), metric="cosine")
    nn.fit(X)
    distances, indices = nn.kneighbors(q_vec)

    results = []
    for rank, (dist, idx) in enumerate(zip(distances[0], indices[0]), start=1):
        row = df.iloc[int(idx)].to_dict()
        compat = round(float((1 - dist) * 10), 1)
        row["rank"] = rank
        row["compatibilidade"] = compat
        results.append(row)
    results.sort(key=lambda r: r["compatibilidade"], reverse=True)

    return jsonify({"consulta": query, "recomendacoes": results})

if __name__ == "__main__":
    ensure_schema()
    app.run(host="0.0.0.0", port=8000, debug=True)
