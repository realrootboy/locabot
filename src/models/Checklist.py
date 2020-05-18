from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from database.main import Database

class Checklist(Database.Base):
    __tablename__ = 'checklists'
    id = Column(Integer, primary_key=True, autoincrement=True)
    motorista_id = Column(Integer, ForeignKey('motoristas.id'))
    motorista = relationship('Motorista', back_populates='checklists')
    is_abertura = Column('is_abertura', Boolean)
    placa = Column('placa', String(255))
    km_inicial = Column('km_inicial', String(255))
    dt_abertura = Column('dt_abertura', DateTime(timezone=True))
    km_final = Column('km_final', String(255))
    dt_fechamento = Column('dt_fechamento', DateTime(timezone=True))
    carro_p_casa = Column('carro_p_casa', Boolean)
    viajou_c_carro = Column('viajou_c_carro', Boolean)
    outro_condutor = Column('outro_condutor', Boolean)
    novo_condutor = Column('novo_condutor', String(255))
    deixou_oficina = Column('deixou_oficina', Boolean)
    local_oficina = Column('local_oficina', String(255))
    van_tacografo = Column('van_tacografo', Boolean)
    calibrou_pneu = Column('calibrou_pneu', Boolean)
    mecanica_motor = Column('mecanica_motor', Boolean)
    mecanica_amortecedor = Column('mecanica_amortecedor', Boolean)
    mecanica_escapamento = Column('mecanica_escapamento', Boolean)
    mecanica_freio = Column('mecanica_freio', Boolean)
    mecanica_embreagem = Column('mecanica_embreagem', Boolean)
    mecanica_acelerador = Column('mecanica_acelerador', Boolean)
    mecanica_cambio = Column('mecanica_cambio', Boolean)
    mecanica_oleo = Column('mecanica_oleo', Boolean)
    mecanica_agua = Column('mecanica_agua', Boolean)
    mecanica_alinhamento = Column('mecanica_alinhamento', Boolean)
    mecanica_freiodemao = Column('mecanica_freiodemao', Boolean)
    lataria_dianteiro = Column('lataria_dianteiro', Boolean)
    lataria_traseiro = Column('lataria_traseiro', Boolean)
    lataria_portadianteiradireita = Column('lataria_portadianteiradireita', Boolean)
    lataria_portadianteiraesquerda = Column('lataria_portadianteiraesquerda', Boolean)
    lataria_portatraseiradireita = Column('lataria_portatraseiradireita', Boolean)
    lataria_portatraseiraesquerda = Column('lataria_portatraseiraesquerda', Boolean)
    lataria_portamalas = Column('lataria_portamalas', Boolean)
    lataria_parachoquedianteiro = Column('lataria_parachoquedianteiro', Boolean)
    lataria_parachoquetraseiro = Column('lataria_parachoquetraseiro', Boolean)
    lataria_capo = Column('lataria_capo', Boolean)
    lataria_teto = Column('lataria_teto', Boolean)
    eletrica_farolete = Column('eletrica_farolete', Boolean)
    eletrica_farolbaixo = Column('eletrica_farolbaixo', Boolean)
    eletrica_farolalto = Column('eletrica_farolalto', Boolean)
    eletrica_setas = Column('eletrica_setas', Boolean)
    eletrica_luzesdopainel = Column('eletrica_luzesdopainel', Boolean)
    eletrica_luzesinternas = Column('eletrica_luzesinternas', Boolean)
    eletrica_bateria = Column('eletrica_bateria', Boolean)
    eletrica_radio = Column('eletrica_radio', Boolean)
    eletrica_altofalantes = Column('eletrica_altofalantes', Boolean)
    eletrica_limpadorparabrisa = Column('eletrica_limpadorparabrisa', Boolean)
    eletrica_arcondicionado = Column('eletrica_arcondicionado', Boolean)
    eletrica_travas = Column('eletrica_travas', Boolean)
    eletrica_vidros = Column('eletrica_vidros', Boolean)
    vidros_parabrisa = Column('vidros_parabrisa', Boolean)
    vidros_lateraisesquerdo = Column('vidros_lateraisesquerdo', Boolean)
    vidros_lateraisdireito = Column('vidros_lateraisdireito', Boolean)
    vidros_traseiro = Column('vidros_traseiro', Boolean)
    seguranca_triangulo = Column('seguranca_triangulo', Boolean)
    seguranca_extintor = Column('seguranca_extintor', Boolean)
    seguranca_cintos = Column('seguranca_cintos', Boolean)
    seguranca_alarme = Column('seguranca_alarme', Boolean)
    seguranca_fechaduras = Column('seguranca_fechaduras', Boolean)
    seguranca_macanetas = Column('seguranca_macanetas', Boolean)
    seguranca_retrovisores = Column('seguranca_retrovisores', Boolean)
    seguranca_macaco = Column('seguranca_macaco', Boolean)
    pneus_dianteiroesquerdo = Column('pneus_dianteiroesquerdo', Boolean)
    pneus_dianteirodireito = Column('pneus_dianteirodireito', Boolean)
    pneus_traseiroesquerdo = Column('pneus_traseiroesquerdo', Boolean)
    pneus_traseirodireito = Column('pneus_traseirodireito', Boolean)
    pneus_estepe = Column('pneus_estepe', Boolean)
    higienizacao_externa = Column('higienizacao_externa', Boolean)
    higienizacao_interna = Column('higienizacao_interna', Boolean)
    
    nao_conformidades = relationship('NaoConformidades', back_populates='checklist')

    def __init__(self,
                 motorista=None,
                 is_abertura=True,
                 placa='',
                 km_inicial='',
                 dt_abertura=None,
                 km_final='',
                 dt_fechamento=None,
                 carro_p_casa=False,
                 viajou_c_carro=False,
                 outro_condutor=False,
                 novo_condutor='',
                 deixou_oficina=False,
                 local_oficina='',
                 van_tacografo=False,
                 calibrou_pneu=False):
        self.motorista = motorista
        self.is_abertura = is_abertura
        self.placa = placa
        self.km_inicial = km_inicial
        self.dt_abertura = dt_abertura
        self.km_final = km_final
        self.dt_fechamento = dt_fechamento
        self.carro_p_casa = carro_p_casa
        self.viajou_c_carro = viajou_c_carro
        self.outro_condutor = outro_condutor
        self.novo_condutor = novo_condutor
        self.deixou_oficina = deixou_oficina
        self.local_oficina = local_oficina
        self.van_tacografo = van_tacografo
        self.calibrou_pneu = calibrou_pneu
