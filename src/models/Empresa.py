from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database



class Empresa(Database.Base):
    __tablename__ = 'empresas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255))
    unidades = relationship('UnidadesEmpresa', back_populates='empresa')
    

    def __init__(self, nome):
        self.nome = nome
