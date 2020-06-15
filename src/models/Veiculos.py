from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class Veiculos(Database.Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    placa = Column('placa', String(255))
    placa_conversao = Column('placa_conversao', String(255))
    marca = Column('marca', String(255))
    modelo = Column('modelo', String(255))
    chassis = Column('chassis', String(255))
    renavam = Column('renavam', String(255))
    situacao = Column('situacao', String(255))
    ano_fabricacao = Column('ano_fabricacao', String(255))
    ano_modelo = Column('ano_modelo', String(255))
    created_at = Column('created_at', DateTime(timezone=True))

    def __init__(self,
                 placa,
                 placa_conversao,
                 marca,
                 modelo,
                 chassis,
                 renavam,
                 situacao,
                 ano_fabricacao,
                 ano_modelo):
        self.placa = placa
        self.placa_conversao = placa_conversao
        self.marca = marca
        self.modelo = modelo
        self.chassis = chassis
        self.renavam = renavam
        self.situacao = situacao
        self.ano_fabricacao = ano_fabricacao
        self.ano_modelo = ano_modelo
        self.created_at = datetime.now(timezone('America/Sao_Paulo'))
