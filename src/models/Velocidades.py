from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database.main import Database

class Velocidades(Database.Base):
    __tablename__ = 'posicionamentos'
    id = Column(Integer, primary_key=True, autoincrement=True)

    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))

    dt_registro = Column('dt_registro', DateTime(timezone=True))
    lat = Column('lat', Float)
    lng = Column('lgn', Float)
    kmh = Column('kmh', Integer)
    local = Column('local', String(255))
    ptref = Column('ptref', String(255))
