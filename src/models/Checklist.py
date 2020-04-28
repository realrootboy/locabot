from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from database.main import Database

class Checklist(Database.Base):
    __tablename__ = 'checklists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates='checklists')
    placa = Column('placa', String(255))
    km_inicial = Column('km_inicial', String(255))
    dt_abertura = Column('dt_abertura', Date())
    km_final = Column('km_final', String(255))
    dt_fechamento = Column('dt_fechamento', Date())
    
    nao_conformidades = relationship('NaoConformidades', back_populates='checklist')

    def __init__(self,
                 motorista=None,
                 placa='',
                 km_inicial='',
                 dt_abertura=None,
                 km_final='',
                 dt_fechamento=None):
        self.motorista = motorista
        self.placa = placa
        self.km_inicial = km_inicial
        self.dt_abertura = dt_abertura
        self.km_final = km_final
        self.dt_fechamento = dt_fechamento
