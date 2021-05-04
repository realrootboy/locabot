from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database


class LogOs(Database.Base):
    __tablename__ = 'log_os'
    id = Column(Integer, primary_key=True, autoincrement=True)
    administrativo_id = Column(Integer, ForeignKey('administrativos.id'))
    os_id = Column(Integer, ForeignKey('ordem_de_servico.id'))
    acao = Column('acao', String(512))

    def __init__(self,
                 acao):
        self.acao = acao
