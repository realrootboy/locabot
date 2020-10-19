from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class Administrativo(Database.Base):
    __tablename__ = 'administrativos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255))
    telegram_user = Column('telegram_user', String(255))
    setor = Column('setor', String(255))
    role = Column('role', String(255))
    pontos_administrativo = relationship('PontosAdministrativo', back_populates='administrativo')
    created_at = Column('created_at', DateTime(timezone=True))
    escalas_administrativo = relationship('EscalasAdministrativo', back_populates='administrativo')
    credenciais = relationship('Credencial', back_populates='administrativo')

    def __init__(self, nome, telegram_user, setor, role):
        self.nome = nome
        self.telegram_user = telegram_user
        self.setor = setor
        self.role = role
        self.created_at = datetime.now(timezone('America/Sao_Paulo'))
