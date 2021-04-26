from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.main import Database

class Patrimonios(Database.Base):
    __tablename__ = 'patrimonios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    prefixo = Column('prefixo', String(255))
    infixo = Column('infixo', String(255))
    descricao = Column('descricao', String(255))
    codigo = Column('codigo', String(255))
    responsavel_atual_id = Column(Integer, ForeignKey('administrativos.id'));
    responsavel_antigo_id = Column(Integer, ForeignKey('administrativos.id'));
    local_uf = Column('local_uf', String(255))
    local_cidade = Column('local_cidade', String(255))
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    dt_aquisicao = Column('dt_aquisicao', DateTime(timezone=True))
    fm_pagamento = Column('fm_pagamento', String(255))
    val_liquido = Column('valor_liquido', String(255))
    vida_util_m = Column('vida_util_m', Integer)

#CREATE TABLE patrimonio (


#    dt_aquisicao
#    fm_pagamento
#    val_liquido
#    vida_util_m
#);