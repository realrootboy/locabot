from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

from models.Account_Administrativo import association_table

class Account(Database.Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column('login', String(255))
    password_hash = Column('password_hash', String(255))
    administrativos = relationship(
        "Administrativo",
        secondary=association_table,
        back_populates="account")

    def __init__(self,
                 login='',
                 password_hash=''):
      self.login = login
      self.password_hash
