from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class Senhas(Database.Base):
    __tablename__ = 'senhas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    login = Column('login', String(255))
    password = Column('password', String(255))
    url = Column('url', String(255))
    observacao = Column('observacao', String(255))

    def __init__(self, login, password, url, observacao):
        self.nome
        self.password
        self.url
        self.observacao
