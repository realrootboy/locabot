from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from database.main import Database

class IdentificacaoFalcao(Database.Base):
    __tablename__ = 'identificacao_falcao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    checklist_id = Column(Integer, ForeignKey('checklists.id'))
    checklist = relationship('Checklist')
    nome = Column('nome', String(255))
    
    def __init__(self,
                checklist,
                nome=''):
        self.checklist = checklist
        self.nome = nome
