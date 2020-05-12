from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database.main import Database

class Checklist(Database.Base):
    __tablename__ = 'checklists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates='checklists')
    placa = Column('placa', String(255))
    km_inicial = Column('km_inicial', String(255))
    dt_abertura = Column('dt_abertura', DateTime(timezone=True))
    km_final = Column('km_final', String(255))
    dt_fechamento = Column('dt_fechamento', DateTime(timezone=True))
    carro_p_casa = Column('carro_p_casa', Boolean)
    viajou_c_carro = Column('viajou_c_carro', Boolean)
    outro_condutor = Column('outro_condutor', Boolean)
    novo_condutor = Column('novo_condutor', String(255))
    deixou_oficina = Column('deixou_oficina', Boolean)
    local_oficina = Column('local_oficina', String(255))
    van_tacografo = Column('van_tacografo', Boolean)
    calibrou_pneu = Column('calibrou_pneu', Boolean)
    
    nao_conformidades = relationship('NaoConformidades', back_populates='checklist')

    def __init__(self,
                 motorista=None,
                 placa='',
                 km_inicial='',
                 dt_abertura=None,
                 km_final='',
                 dt_fechamento=None,
                 carro_p_casa=False,
                 viajou_c_carro=False,
                 outro_condutor=False,
                 novo_condutor='',
                 deixou_oficina=False,
                 local_oficina='',
                 van_tacografo=False,
                 calibrou_pneu=False):
        self.motorista = motorista
        self.placa = placa
        self.km_inicial = km_inicial
        self.dt_abertura = dt_abertura
        self.km_final = km_final
        self.dt_fechamento = dt_fechamento
        self.carro_p_casa = carro_p_casa
        self.viajou_c_carro = viajou_c_carro
        self.outro_condutor = outro_condutor
        self.novo_condutor = novo_condutor
        self.deixou_oficina = deixou_oficina
        self.local_oficina = local_oficina
        self.van_tacografo = van_tacografo
        self.calibrou_pneu = calibrou_pneu
