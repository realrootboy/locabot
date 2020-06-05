from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class Administrativo(Database.Base):
    __tablename__ = 'administrativo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255))
    telegram_user = Column('telegram_user', String(255))
    role = Column('role', String(255))
    created_at = Column('created_at', DateTime(timezone=True))

    def __init__(self, nome, telegram_user, role):
        self.nome = nome
        self.telegram_user = telegram_user
        self.role = role
        self.created_at = datetime.now(timezone('America/Sao_Paulo'))