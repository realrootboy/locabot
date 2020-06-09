from database.main import Database

from models.Motorista import Motorista
from models.PontosMotorista import PontosMotorista
from models.IntervalosDePontoMotorista import IntervalosDePontoMotorista
from models.Administrativo import Administrativo
from models.Checklist import Checklist
from models.NaoConformidades import NaoConformidades
from models.Veiculos import Veiculos
from models.Registro import Registro
from models.EscalasMotorista import EscalasMotorista

def main():
    print("creating tables...")
    Database.Base.metadata.create_all(Database.engine)

main()