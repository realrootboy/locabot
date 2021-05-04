from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import relationship

from database.main import Database

association_table = Table('pessoas_ordem', Database.Base.metadata,
    Column('ordem_id', Integer, ForeignKey('ordem_de_servico.id')),
    Column('pessoa_id', Integer, ForeignKey('pessoas_empresa.id'))
)

class Passageiros(Database.Base):
    __tablename__ = 'passageiros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255))
    cc = Column('cc', DECIMAL)
    os_id = Column(Integer, ForeignKey('ordem_de_servico.id'))

    def __init__(self, os, nome):
        self.os = os
        self.nome = nome
