from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class PontosAdministrativo(Database.Base):
    __tablename__ = 'pontos_administrativo'
    id = Column(Integer, primary_key=True, autoincrement=True)
    administrativo_id = Column(Integer, Database.Base.metadata, ForeignKey('administrativos.id'))
    administrativo = relationship('Administrativo', back_populates='pontos_administrativo')
    entrada = Column('entrada', DateTime(timezone=True))
    saida = Column('saida', DateTime(timezone=True))
    horas_trabalhadas = Column('horas_trabalhadas', String(255))
    horas_extra = Column('horas_extra', String(255))
    intervalos_de_ponto_administrativo = relationship('IntervalosDePontoAdministrativo', back_populates='ponto')

    def __init__(self,
                 administrativo,
                 entrada,
                 saida,
                 horas_trabalhadas=None,
                 horas_extra=None):
        self.administrativo = administrativo
        self.entrada = entrada
        self.saida = saida
        self.horas_trabalhadas = horas_trabalhadas
        self.horas_extra = horas_extra

    


#  
# datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
# date1 = '2016-04-16 10:01:28.585'
# date2 = '2016-03-10 09:56:28.067'
# diff = datetime.datetime.strptime(date1, datetimeFormat)\
#     - datetime.datetime.strptime(date2, datetimeFormat)
#
# diff.total_seconds()
# def convert(seconds): 
#     seconds = seconds % (24 * 3600) 
#     hour = seconds // 3600
#     seconds %= 3600
#     minutes = seconds // 60
#     seconds %= 60
#     return "%d:%02d:%02d" % (hour, minutes, seconds) 