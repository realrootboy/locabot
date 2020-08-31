from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, Integer, Date, Table, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from database.main import Database

class DesviosMotorista(Database.Base):
    __tablename__ = 'desvios_motorista'
    id = Column(Integer, primary_key=True, autoincrement=True)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship(
        'Motorista', back_populates='desvios')
    descricao = Column('descricao', String(255))
    causa = Column('causa', String(255))
    gerou_retrabalho = Column('gerou_retrabalho', String(255))
    acao_a_ser_tomada = Column('acao_a_ser_tomada', String(255))
    responsavel_id = Column(Integer, ForeignKey('administrativos.id'))
    responsavel = relationship(
        'Administrativo')
    prev_imp = Column('prev_imp', DateTime(timezone=True))
    eficaz = Column('eficaz', String(255))
    obs = Column('obs', String(255))
    created_at = Column('created_at', DateTime(timezone=True))

    def __init__(self,
                 motorista,
                 descricao, 
                 causa,
                 gerou_retrabalho,
                 acao_a_ser_tomada,
                 responsavel,
                 prev_imp,
                 eficaz,
                 obs):
        self.motorista = motorista
        self.descricao = descricao
        self.causa = causa
        self.gerou_retrabalho = gerou_retrabalho
        self.acao_a_ser_tomada = acao_a_ser_tomada
        self.responsavel = responsavel
        self.prev_imp = prev_imp
        self.eficaz = eficaz
        self.created_at = datetime.now(timezone('America/Sao_Paulo'))
