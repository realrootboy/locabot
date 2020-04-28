from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey
from sqlalchemy.orm import relationship

from database.main import Database

class NaoConformidades(Database.Base):
    __tablename__ = 'nao_conformidades'
    id = Column(Integer, primary_key=True, autoincrement=True)
    checklist_id = Column(Integer, ForeignKey('checklists.id'))
    checklist = relationship('Checklist', back_populates="nao_conformidades")
    path = Column('path', String(255))
    descricao = Column('path', String(255))

    def __init__(self,
                path='',
                descricao=''):
        self.path = path
        self.descricao = descricao