from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class Categorias(Database.Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255))
    created_at = Column('created_at', DateTime(timezone=True))

    def __init__(self, nome):
        self.nome = nome;
        self.created_at = datetime.now(timezone('America/Sao_Paulo'))