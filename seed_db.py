
import os, random
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, Mentor

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") or "sqlite:///mentoria.db"
engine = create_engine(DATABASE_URL, echo=False, future=True)

cursos = {
    "Computação": ["IA","Banco de Dados","Redes","Segurança","UX","Produto"],
    "Engenharia": ["Automação","Redes","IA","Gestão de Projetos"],
    "Psicologia": ["Orientação Acadêmica","Carreira","Neuropsicologia"],
    "Design": ["UX","UI","Produto","Motion"],
    "Administração": ["Finanças","Projetos","Empreendedorismo","Marketing"]
}
disps = ["Manhã","Tarde","Noite"]
insts = ["USP","UFSC","UFRJ","UFMG","UFPR","UFBA","PUC"]

def seed(n=80):
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        # limpa tabela
        s.query(Mentor).delete()
        idx = 1
        for curso, interesses in cursos.items():
            for i in range(n//len(cursos)):
                m = Mentor(
                    nome=f"Prof. {curso} {i+1}",
                    curso=curso,
                    interesse=random.choice(interesses),
                    disponibilidade=random.choice(disps),
                    instituicao=random.choice(insts)
                )
                s.add(m)
                idx += 1
        s.commit()
    print("Seed concluído.")

if __name__ == "__main__":
    seed()
