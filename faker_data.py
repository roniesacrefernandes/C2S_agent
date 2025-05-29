import random
import datetime
from faker import Faker
from sqlalchemy.orm import Session

from database.connections import get_db, create_tables
from database.models import Automovel
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

fake = Faker('pt_BR')

def generate_fake_automovel_data():
    """
    Gera um dicionário com dados fictícios
    """
    marcas = ['Toyota', 'Honda', 'Volkswagen', 'Chevrolet', 'Ford', 'Hyundai', 'Renault', 'Fiat', 'Jeep', 'BMW', 'Mercedes-Benz', 'Audi']
    tipos_combustivel = ['Gasolina', 'Etanol', 'Flex', 'Diesel', 'Elétrico', 'Híbrido']
    cores = ['Preto', 'Branco', 'Prata', 'Cinza', 'Vermelho', 'Azul', 'Verde', 'Amarelo']
    tipo_cambio = ['Automática', 'Manual', 'Semi-Automática']

    marca = random.choice(marcas)
    if marca == 'Toyota':
        modelo = random.choice(['Corolla', 'Hilux', 'RAV4', 'Yaris'])
    elif marca == 'Honda':
        modelo = random.choice(['Civic', 'HR-V', 'CR-V', 'Fit'])
    elif marca == 'Volkswagen':
        modelo = random.choice(['Gol', 'Virtus', 'T-Cross', 'Amarok'])
    elif marca == 'Chevrolet':
        modelo = random.choice(['Onix', 'Tracker', 'S10', 'Cruze'])
    elif marca == 'Ford':
        modelo = random.choice(['Ka', 'Ranger', 'EcoSport', 'Focus'])
    elif marca == 'Hyundai':
        modelo = random.choice(['HB20', 'Creta', 'Tucson'])
    elif marca == 'Fiat':
        modelo = random.choice(['Argo', 'Cronos', 'Strada', 'Toro'])
    elif marca == 'Jeep':
        modelo = random.choice(['Renegade', 'Compass'])
    else:
        modelo = fake.word().capitalize() + ' ' + str(random.randint(100, 999))

    return {
        "marca": marca,
        "modelo": modelo,
        "ano": random.randint(2000, datetime.datetime.now().year + 1),
        "quilometragem": round(random.uniform(0, 200000), 2),        
        "tipo_combustivel": random.choice(tipos_combustivel),
        "tipo_cambio": random.choice(tipo_cambio),
        "cor": random.choice(cores),
        "numero_portas": random.choice([2, 4]),
        "tem_multa": random.choice(['S', 'N']),
        "valor": round(random.uniform(30000, 250000), 2),
        "data_revisao": fake.date_time_between(start_date='-5y', end_date='now')
    }

def insert_fake_automoveis(num_records: int):

    create_tables()

    db: Session = next(get_db())
    try:
        print(f"Gerando e inserindo {num_records} registros de automóveis")
        for i in range(num_records):
            automovel_data = generate_fake_automovel_data()
            automovel = Automovel(**automovel_data)
            db.add(automovel)
            if (i + 1) % 100 == 0:
                db.commit()
        db.commit()
        print(f"Total de {num_records} registros inseridos")
    except Exception as e:
        db.rollback()
        print(f"Ocorreu um erro: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    num_registros_a_gerar = 100
    insert_fake_automoveis(num_registros_a_gerar)
