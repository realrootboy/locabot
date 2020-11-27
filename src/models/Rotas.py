from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class Rotas(Database.Base):
    __tablename__ = 'rotas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column('nome', String(255))
    cep = Column('cep', String(255))
    endereco = Column('endereco', String(255))
    bairro = Column('bairro', String(255))
    cidade = Column('cidade', String(255))
    uf = Column('uf', String(255))
    url = Column('url', String(255))

    def __init__(self, nome, cep, endereco, bairro, cidade, uf, url):
        self.nome = nome
        self.cep = cep
        self.endereco = endereco
        self.bairro = bairro
        self.cidade = cidade
        self.uf = uf
        self.url = url

    