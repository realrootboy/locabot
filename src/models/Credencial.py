from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

from models.Administrativo import Administrativo

class Credencial(Database.Base):
    __tablename__ = "credenciais"
    id = Column(Integer, primary_key=True, autoincrement=True)
    administrativo_id = Column(Integer, ForeignKey('administrativos.id'))
    administrativo = relationship('Administrativo', back_populates="credenciais")
    password_hash = Column('password_hash', String(255))
    
    def __init__(self, administrativo, password_hash):
        self.administrativo = administrativo
        self.password_hash = password_hash
