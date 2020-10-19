from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

from models.Pessoas_Ordem import association_table

class PessoasEmpresa(Database.Base):
    __tablename__ = 'pessoas_empresa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    unidade_empresa_id = Column(Integer, ForeignKey('unidades_empresa.id'))
    empresa = relationship('UnidadesEmpresa', back_populates='pessoas')
    nome = Column('nome', String(255))
    role = Column('role', String(255))

    ordens = relationship(
        "OrdemDeServico",
        secondary=association_table,
        back_populates="passageiros")

    def __init__(self, empresa, nome):
        self.empresa = empresa
        self.nome = nome
