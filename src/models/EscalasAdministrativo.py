from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class EscalasAdministrativo(Database.Base):
    __tablename__ = 'escalas_administrativo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    administrativo_id = Column(Integer, ForeignKey('administrativos.id'))
    administrativo = relationship('Administrativo', back_populates="escalas_administrativo")
    escala = Column('escala', String(100))
    vigencia = Column('vigencia', DateTime(timezone=True))
    fim_vigencia = Column('fim_vigencia', DateTime(timezone=True))

    def __init__(self,
                 administrativo,
                 escala,
                 vigencia,
                 fim_vigencia):
        self.administrativo = administrativo
        self.escala = escala
        self.vigencia = vigencia
        self.fim_vigencia = fim_vigencia