from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

from database.main import Database

class Tags(Database.Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, autoincrement=True)

    idd = Column('idd', String(255))
    ic = Column('ic', String(255))
    empresa = Column('empresa', String(255))
    

