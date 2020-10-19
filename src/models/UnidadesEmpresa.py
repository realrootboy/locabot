from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database


class UnidadesEmpresa(Database.Base):
    __tablename__ = 'unidades_empresa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    empresa_id = Column(Integer, ForeignKey('empresas.id'))
    empresa = relationship('Empresa', back_populates='unidades')
    pessoas = relationship('PessoasEmpresa', back_populates='empresa')
    nome = Column('nome', String(255))

    def __init__(self, empresa, nome):
        self.empresa = empresa
        self.nome = nome
