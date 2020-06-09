from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database


class PontosMotorista(Database.Base):
    __tablename__ = 'pontos_motorista'
    id = Column(Integer, primary_key=True, autoincrement=True)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates='pontos_motorista')
    entrada = Column('entrada', DateTime(timezone=True))
    saida = Column('saida', DateTime(timezone=True))
    horas_trabalhadas = Column('horas_trabalhadas', String(255))
    horas_extra = Column('horas_extra', String(255))
    intervalos_de_ponto_motorista = relationship('IntervalosDePontoMotorista', back_populates='ponto')

    def __init__(self,
                 motorista,
                 entrada,
                 saida):
        self.motorista = motorista
        self.entrada = entrada
        self.saida = saida



# import datetime
# from datetime import timedelta
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