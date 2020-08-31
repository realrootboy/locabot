from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class Motorista(Database.Base):
    __tablename__ = 'motoristas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255))
    telegram_user = Column('telegram_user', String(255))
    registros = relationship('Registro', back_populates='motorista')
    desvios = relationship('DesviosMotorista', back_populates='motorista')
    checklists = relationship('Checklist', back_populates='motorista')
    pontos_motorista = relationship('PontosMotorista', back_populates='motorista')
    escalas_motorista = relationship('EscalasMotorista', back_populates='motorista')
    created_at = Column('created_at', DateTime(timezone=True))

    def __init__(self, nome, telegram_user):
        self.nome = nome
        self.telegram_user = telegram_user
        self.created_at = datetime.now(timezone('America/Sao_Paulo'))
