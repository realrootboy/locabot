from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database


class PontosMotorista(Database.Base):
    __tablename__ = 'pontos_motorista'
    id = Column(Integer, primary_key=True, autoincrement=True)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates='pontos_motorista')
    entrada = Column('entrada', DateTime(timezone=True))
    saida = Column('saida', DateTime(timezone=True))
    intervalos_de_ponto_motorista = relationship('IntervalosDePontoMotorista', back_populates='ponto')

    def __init__(self,
                 motorista,
                 entrada,
                 saida):
        self.motorista = motorista
        self.entrada = entrada
        self.saida = saida
