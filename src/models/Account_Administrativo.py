from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

association_table = Table('account_administrativo', Database.Base.metadata,
    Column('administrativo_id', Integer, ForeignKey('administrativos.id')),
    Column('account_id', Integer, ForeignKey('accounts.id'))
)


