from database.main import Database

from models.Motorista import Motorista
from models.PontosMotorista import PontosMotorista
from models.IntervalosDePontoMotorista import IntervalosDePontoMotorista
from models.EscalasMotorista import EscalasMotorista

from models.Administrativo import Administrativo
from models.PontosAdministrativo import PontosAdministrativo
from models.IntervalosDePontoAdministrativo import IntervalosDePontoAdministrativo
from models.EscalasAdministrativo import EscalasAdministrativo

from models.Registro import Registro
from models.Checklist import Checklist
from models.NaoConformidades import NaoConformidades
from models.IdentificacaoFalcao import IdentificacaoFalcao

from models.Credencial import Credencial

from models.Veiculos import Veiculos

from models.DesviosAdministrativo import DesviosAdministrativo
from models.DesviosMotorista import DesviosMotorista

# from models.Empresa import Empresa
# from models.PessoasEmpresa import PessoasEmpresa
# from models.UnidadesEmpresa import UnidadesEmpresa
# 
# from models.OrdemDeServico import OrdemDeServico

from models.Categorias import Categorias
from models.CategoriasAdministrativo import *
from models.Senhas import Senhas

def main():
    loadDb()

def loadDb():
    Database.Base.metadata.create_all(Database.engine)

main()
