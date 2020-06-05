from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database


class IntervalosDePontoMotorista(Database.Base):
    __tablename__ = 'intervalos_de_ponto_motorista'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ponto_motorista_id = Column(Integer, ForeignKey('pontos_motorista.id'))
    ponto = relationship('PontosMotorista', back_populates='intervalos_de_ponto_motorista')
    intervalo = Column('intervalo', DateTime(timezone=True))
    fim_intervalo = Column('fim_intervalo', DateTime(timezone=True))

    def __init__(self,
                 ponto,
                 intervalo,
                 fim_intervalo):
        self.ponto = ponto
        self.intervalo = intervalo
        self.fim_intervalo = fim_intervalo
