from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

from models.Pessoas_Ordem import association_table

class OrdemDeServico(Database.Base):
    __tablename__ = 'ordem_de_servico'
    id = Column(Integer, primary_key=True, autoincrement=True)
    administrativo_id = Column(Integer, ForeignKey('administrativos.id'))

    tipo_de_ordem = Column('tipo_de_ordem', String(255))

    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates='ordens')
    veiculo_id = Column(Integer, ForeignKey('veiculos.id'))
    empresa_id = Column(Integer, ForeignKey('empresas.id'))

    unidade_id = Column(Integer, ForeignKey('unidades_empresa.id'))
    
    coordenador_id = Column(Integer, ForeignKey('pessoas_empresa.id'))
    solicitante_id = Column(Integer, ForeignKey('pessoas_empresa.id'))
    
    categoria = Column('categoria', String(255))

    situacao = Column('situacao', String(255))
    

    dt_servico = Column('dt_servico', DateTime(timezone=True))
    observacao = Column('observacao', String(255))

    fk_rota_1 = Column(Integer, ForeignKey('rotas.id'))
    fk_rota_2 = Column(Integer, ForeignKey('rotas.id'))



    passageiros = relationship(
        "PessoasEmpresa",
        secondary=association_table,
        back_populates="ordens")
    

    def __init__(self,
                motorista,
                veiculo):
        self.motorista = motorista
        self.veiculo = veiculo


