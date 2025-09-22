
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass

class Mentor(Base):
    __tablename__ = "mentores"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(120))
    curso: Mapped[str] = mapped_column(String(60), index=True)
    interesse: Mapped[str] = mapped_column(String(80), index=True)
    disponibilidade: Mapped[str] = mapped_column(String(20), index=True)
    instituicao: Mapped[str] = mapped_column(String(40), index=True)
