# models.py
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Automovel(Base):
    __tablename__ = 'automoveis'

    id = Column(Integer, primary_key=True, autoincrement=True)
    marca = Column(String(50), nullable=False)
    modelo = Column(String(50), nullable=False)
    ano = Column(Integer, nullable=False)
    quilometragem = Column(Float, nullable=False)
    tipo_combustivel = Column(String(30), nullable=False)
    tipo_cambio = Column(String(30), nullable=False)
    cor = Column(String(30), nullable=False)
    numero_portas = Column(Integer, nullable=False)
    tem_multa = Column(String(1), nullable=False) # 'S' para sim, 'N' para não
    valor = Column(Float, nullable=False)
    data_revisao = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (f"<Automovel(marca='{self.marca}', modelo='{self.modelo}', "
                f"ano={self.ano}, valor={self.valor})>")