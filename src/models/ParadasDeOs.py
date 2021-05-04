from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class ParadasDeOs(Database.Base):
    __tablename__ = 'paradas_de_os'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ordem_de_servico_id = Column(Integer, ForeignKey('ordem_de_servico.id'))
    fk_rota = Column(Integer, ForeignKey('rotas.id'))
