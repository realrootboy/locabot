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
    intervalo = Column('intervalo', DateTime(timezone=True))
    fim_intervalo = Column('fim_intervalo', DateTime(timezone=True))
    saida = Column('saida', DateTime(timezone=True))

    def __init__(self,
                 motorista,
                 entrada,
                 intervalo,
                 fim_intervalo,
                 saida):
        self.motorista = motorista
        self.entrada = entrada
        self.intervalo = intervalo
        self.fim_intervalo = fim_intervalo
        self.saida = saida
