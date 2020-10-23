from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database.main import Database

class Deslocamentos(Database.Base):
    __tablename__ = 'deslocamentos'
    id = Column(Integer, primary_key=True, autoincrement=True)

    evento = Column('evento', String(255))

    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))

    hr_inicio = Column('hr_inicio', DateTime(timezone=True))
    hr_final = Column('hr_final', DateTime(timezone=True))

    duracao = Column('duracao', String(255))
    distancia = Column('distancia', Integer)

    localini = Column('localini', String(255))
    refini = Column('refini', String(255))
    localfim = Column('localfim', String(255))
    reffim = Column('reffim', String(255))
