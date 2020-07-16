from database.main import Database

from models.Motorista import Motorista
from models.PontosMotorista import PontosMotorista
from models.IntervalosDePontoMotorista import IntervalosDePontoMotorista
from models.EscalasMotorista import EscalasMotorista

from models.Administrativo import Administrativo
from models.PontosAdministrativo import PontosAdministrativo
from models.IntervalosDePontoAdministrativo import IntervalosDePontoAdministrativo

from models.Registro import Registro
from models.Checklist import Checklist
from models.NaoConformidades import NaoConformidades

from models.Account import Account
from models.Credencial import Credencial

from models.Veiculos import Veiculos

def main():
    print("creating tables...")
    loadDb()

def loadDb():
    Database.Base.metadata.create_all(Database.engine)

main()
