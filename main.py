import random
import datetime
from faker import Faker
from models.automovel import Automovel 
from database.connection import Session, create_tables

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

def populate_automoveis_data(num_veiculos: int = 100):
    """
    Popula o banco de dados com um número especificado de veículos fictícios.
    """
    session = Session()

    print(f"Gerando veículos fictícios...")

    try:
        for _ in range(num_veiculos):
            data = generate_fake_automovel_data()
            automovel = Automovel(**data)
            session.add(automovel)

        session.commit()
        print(f"{num_veiculos} veículos inseridos com sucesso!")
    except Exception as e:
        session.rollback()
        print(f"Erro ao inserir veículos: {e}")
    finally:
        session.close()

def main():
    """
    criação do banco de dados e
    população de dados.
    """
    print("Iniciando o script de automóveis...")

    create_tables()

    populate_automoveis_data(num_veiculos=100)

    print("\nProcesso concluído. O banco de dados 'automoveis.db' está pronto em ./data/")

if __name__ == "__main__":
    main()