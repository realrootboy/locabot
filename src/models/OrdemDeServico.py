from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

from models.Pessoas_Ordem import association_table

class OrdemDeServico(Database.Base):
    __tablename__ = 'ordem_de_servico'
    id = Column(Integer, primary_key=True, autoincrement=True)

    tipo_de_ordem = Column('tipo_de_ordem', String(255))

    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates='ordens')
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    empresa_id = Column(Integer, ForeignKey('empresas.id'))

    unidade_id = Column(Integer, ForeignKey('unidades_empresa.id'))
    
    coordenador_id = Column(Integer, ForeignKey('pessoas_empresa.id'))
    solicitante_id = Column(Integer, ForeignKey('pessoas_empresa.id'))
    
    situacao = Column('situacao', String(255))
    origem = Column('origem', String(255))
    destino = Column('destino', String(255))
    dt_servico = Column('dt_servico', DateTime(timezone=True))
    observacao = Column('observacao', String(255))


    passageiros = relationship(
        "PessoasEmpresa",
        secondary=association_table,
        back_populates="ordens")
    

    def __init__(self,
                motorista,
                veiculo):
        self.motorista = motorista
        self.veiculo = veiculo


