from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database.main import Database

class Pedagios(Database.Base):
    __tablename__ = 'pedagios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    tag_id = Column(Integer, ForeignKey('tags.id'))
    data_hora = Column('data_hora', DateTime(timezone=True))
    rodovia = Column('rodovia', String(255))
    praca = Column('praca', String(255))
    valor = Column('valor', String(255))
