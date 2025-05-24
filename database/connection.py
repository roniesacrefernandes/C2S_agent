import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.automovel import Base 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'automoveis.db')
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Cria uma instância do mecanismo de banco de dados.
engine = create_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """
    Cria tabelas definidas nos modelos no banco de dados.
    """
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

    if os.path.exists(DATABASE_PATH):
        os.remove(DATABASE_PATH)
        print(f"Arquivo de banco de dados '{DATABASE_PATH}' existente removido.")

    Base.metadata.create_all(engine)
    print("Tabelas do banco de dados criadas com sucesso!")