from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Automovel(Base):
    """
    Esquema da tabela 'automoveis';
    """
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
    tem_multa = Column(String(1), nullable=False)
    valor = Column(Float, nullable=False)
    data_revisao = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return (f"<Automovel(marca='{self.marca}', modelo='{self.modelo}', "
                f"ano={self.ano}, quilometragem='{self.quilometragem}')>")