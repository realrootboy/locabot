from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class EscalasMotorista(Database.Base):
    __tablename__ = 'escalas_motorista'
    id = Column(Integer, primary_key=True, autoincrement=True)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates="escalas_motorista")
    escala = Column('escala', String(7))

    def __init__(self,
                 motorista,
                 escala):
        self.motorista = motorista
        self.escala = escala