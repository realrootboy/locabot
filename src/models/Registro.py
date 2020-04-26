from datetime import datetime

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from database.main import Database

class Registro(Database.Base):
    __tablename__ = 'registros'
    id = Column(Integer, primary_key=True, autoincrement=True)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates="registros")
    placa = Column('placa', String(255))
    quilometragem = Column('quilometragem', String(255))
    qnt_litro = Column('qnt_litro', String(255))
    val_litro = Column('val_litro', String(255))
    val_total = Column('val_total', String(255))
    tp_combustivel = Column('tp_combustivel', String(255))
    posto = Column('posto', String(255))
    media_dir = Column('media_dir', String(255))

    def __init__(self,
                 motorista,
                 placa='',
                 quilometragem='',
                 qnt_litro='',
                 val_litro='',
                 val_total='',
                 tp_combustivel='',
                 posto='',
                 media_dir=''):
        self.motorista = motorista
        self.placa = placa
        self.quilometragem = quilometragem
        self.qnt_litro = qnt_litro
        self.val_litro = val_litro
        self.val_total = val_total
        self.tp_combustivel = tp_combustivel
        self.posto = posto
        self.media_dir = media_dir