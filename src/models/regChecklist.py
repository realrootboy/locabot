from datetime import datetime
from pytz import timezone


def strBool(b):
    if(b):
        return 'Sim'
    else:
        return 'Não'


def strBool2(b):
    if(b):
        return 'Ok'
    else:
        return 'Não está ok'

ASSOC = {
    'mecanica': [('mecanica','Mecânica'),
                ('motor','Motor'),
                ('amortecedor','Amortecedor'),
                ('escapamento','Escapamento'),
                ('freio','Freio'),
                ('embreagem','Embreagem'),
                ('acelerador','Acelerador'),
                ('cambio','Câmbio'),
                ('oleo','Òleo'),
                ('agua','Agua'),
                ('alinhamento','Alinhamento'),
                ('freiodemao','Freio de mão')],
    'lataria': [('lataria','Lataria'),
                ('dianteiro','Lataria dianteira'),
                ('traseiro','Lateria traseira'),
                ('portadianteiradireita','Porta dianteira direita'),
                ('portadianteiraesquerda','Porta dianteira esquerda'),
                ('portatraseiradireita','Porta traseira direita'),
                ('portatraseiraesquerda','Porta traseira esquerda'),
                ('portamalas','Porta-malas'),
                ('parachoquedianteiro','Parachoque dianteiro'),
                ('parachoquetraseiro', 'Parachoque traseiro')],
    'eletrica': [('eletrica','Elétrica'),
                ('farolete','Farolete'),
                ('farolbaixo','Farol baixo'),
                ('farolalto','Farol alto'),
                ('setas','Setas'),
                ('luzesdopainel','Luzes do painel'),
                ('luzesinternas','Luzes internas'),
                ('bateria','Bateria'),
                ('radio','Radio'),
                ('altofalantes','Alto falantes'),
                ('limpadorparabrisa','Limpador de parabrisa'),
                ('arcondicionado','Ar condicionado'),
                ('travas','Travas'),
                ('vidros', 'Vidros')],
    'vidros': [('vidros','Vidros'),
                ('parabrisa','Parabrisa'),
                ('lateraisesquerdo','Laterais esquerdo'),
                ('lateraisdireito','Laterais direito'),
                ('traseiro', 'Traseiro')],
    'seguranca': [('seguranca','Segurança'),
                ('triangulo','Triangulo'),
                ('extintor','Extintor'),
                ('cintos','Cintos'),
                ('alarme','Alarme'),
                ('fechaduras','Fechaduras'),
                ('macanetas','Maçanetas'),
                ('retrovisores','Retrovisores'),
                ('macaco', 'Macaco')],
    'pneus': [('pneus','Pneus'),
                ('dianteiroesquerdo','Dianteiro esquerdo'),
                ('dianteirodireito','Dianteiro direito'),
                ('traseiroesquerdo','Traseiro esquerdo'),
                ('traseiroedireito','Traseiro direito'),
                ('estepe', 'Estepe')],
    'higienizacao': [('higienizacao','Higienização'),
                ('externa','Higienização externa'),
                ('interna','Higienização interna')]
}

class RegChecklist:

    def __init__(self,
                 username,
                 chat_id,
                 is_abertura,
                 placa='',
                 km_inicial='',
                 dt_abertura=datetime.now(timezone('America/Sao_Paulo')),
                 km_final='',
                 motivo='',
                 manual=True,
                 crlv=True,
                 chave_reserva=False,
                 dt_fechamento=None,
                 idd=-1,
                 motorista_id=-1,
                 carro_p_casa=False,
                 viajou_c_carro=False,
                 outro_condutor=False,
                 novo_condutor='',
                 deixou_oficina=False,
                 local_oficina='',
                 van_tacografo=False,
                 calibrou_pneu=False,
                 mecanica_motor=True,
                 mecanica_amortecedor=True,
                 mecanica_escapamento=True,
                 mecanica_freio=True,
                 mecanica_embreagem=True,
                 mecanica_acelerador=True,
                 mecanica_cambio=True,
                 mecanica_oleo=True,
                 mecanica_agua=True,
                 mecanica_alinhamento=True,
                 mecanica_freiodemao=True,
                 lataria_dianteiro=True,
                 lataria_traseiro=True,
                 lataria_portadianteiradireita=True,
                 lataria_portadianteiraesquerda=True,
                 lataria_portatraseiradireita=True,
                 lataria_portatraseiraesquerda=True,
                 lataria_portamalas=True,
                 lataria_parachoquedianteiro=True,
                 lataria_parachoquetraseiro=True,
                 lataria_capo=True,
                 lataria_teto=True,
                 eletrica_farolete=True,
                 eletrica_farolbaixo=True,
                 eletrica_farolalto=True,
                 eletrica_setas=True,
                 eletrica_luzesdopainel=True,
                 eletrica_luzesinternas=True,
                 eletrica_bateria=True,
                 eletrica_radio=True,
                 eletrica_altofalantes=True,
                 eletrica_limpadorparabrisa=True,
                 eletrica_arcondicionado=True,
                 eletrica_travas=True,
                 eletrica_vidros=True,
                 vidros_parabrisa=True,
                 vidros_lateraisesquerdo=True,
                 vidros_lateraisdireito=True,
                 vidros_traseiro=True,
                 seguranca_triangulo=True,
                 seguranca_extintor=True,
                 seguranca_cintos=True,
                 seguranca_alarme=True,
                 seguranca_fechaduras=True,
                 seguranca_macanetas=True,
                 seguranca_retrovisores=True,
                 seguranca_macaco=True,
                 pneus_dianteiroesquerdo=True,
                 pneus_dianteirodireito=True,
                 pneus_traseiroesquerdo=True,
                 pneus_traseirodireito=True,
                 pneus_estepe=True,
                 higienizacao_externa=True,
                 higienizacao_interna=True,
                 cache_id = -1,
                 cache_field = '',
                 cache_group = '',
                 nome_falcao = '',
                 ):
        self.username = username
        self.chat_id = chat_id
        self.is_abertura = is_abertura
        self.placa = placa
        self.km_inicial = km_inicial
        self.dt_abertura = datetime.now(timezone('America/Sao_Paulo'))
        self.km_final = km_final
        self.motivo = motivo
        self.manual = manual
        self.crlv = crlv
        self.chave_reserva = chave_reserva
        self.dt_fechamento = dt_fechamento
        self.id = idd
        self.motorista_id = motorista_id
        self.n_conformidades = 0
        self.media_dir = str(datetime.now(timezone('America/Sao_Paulo'))) + ' ' + username
        self.desc_conformidades = list()
        self.carro_p_casa = carro_p_casa
        self.viajou_c_carro = viajou_c_carro
        self.outro_condutor = outro_condutor
        self.novo_condutor = novo_condutor
        self.deixou_oficina = deixou_oficina
        self.local_oficina = local_oficina
        self.van_tacografo = van_tacografo
        self.calibrou_pneu = calibrou_pneu
        self.mecanica_motor = mecanica_motor
        self.mecanica_amortecedor = mecanica_amortecedor
        self.mecanica_escapamento = mecanica_escapamento
        self.mecanica_freio = mecanica_freio
        self.mecanica_embreagem = mecanica_embreagem
        self.mecanica_acelerador = mecanica_acelerador
        self.mecanica_cambio = mecanica_cambio
        self.mecanica_oleo = mecanica_oleo
        self.mecanica_agua = mecanica_agua
        self.mecanica_alinhamento = mecanica_alinhamento
        self.mecanica_freiodemao = mecanica_freiodemao
        self.lataria_dianteiro = lataria_dianteiro
        self.lataria_traseiro = lataria_traseiro
        self.lataria_portadianteiradireita = lataria_portadianteiradireita
        self.lataria_portadianteiraesquerda = lataria_portadianteiraesquerda
        self.lataria_portatraseiradireita = lataria_portatraseiradireita
        self.lataria_portatraseiraesquerda = lataria_portatraseiraesquerda
        self.lataria_portamalas = lataria_portamalas
        self.lataria_parachoquedianteiro = lataria_parachoquedianteiro
        self.lataria_parachoquetraseiro = lataria_parachoquetraseiro
        self.lataria_capo = lataria_capo
        self.lataria_teto = lataria_teto
        self.eletrica_farolete = eletrica_farolete
        self.eletrica_farolbaixo = eletrica_farolbaixo
        self.eletrica_farolalto = eletrica_farolalto
        self.eletrica_setas = eletrica_setas
        self.eletrica_luzesdopainel = eletrica_luzesdopainel
        self.eletrica_luzesinternas = eletrica_luzesinternas
        self.eletrica_bateria = eletrica_bateria
        self.eletrica_radio = eletrica_radio
        self.eletrica_altofalantes = eletrica_altofalantes
        self.eletrica_limpadorparabrisa = eletrica_limpadorparabrisa
        self.eletrica_arcondicionado = eletrica_arcondicionado
        self.eletrica_travas = eletrica_travas
        self.eletrica_vidros = eletrica_vidros
        self.vidros_parabrisa = vidros_parabrisa
        self.vidros_lateraisesquerdo = vidros_lateraisesquerdo
        self.vidros_lateraisdireito = vidros_lateraisdireito
        self.vidros_traseiro = vidros_traseiro
        self.seguranca_triangulo = seguranca_triangulo
        self.seguranca_extintor = seguranca_extintor
        self.seguranca_cintos = seguranca_cintos
        self.seguranca_alarme = seguranca_alarme
        self.seguranca_fechaduras = seguranca_fechaduras
        self.seguranca_macanetas = seguranca_macanetas
        self.seguranca_retrovisores = seguranca_retrovisores
        self.seguranca_macaco = seguranca_macaco
        self.pneus_dianteiroesquerdo = pneus_dianteiroesquerdo
        self.pneus_dianteirodireito = pneus_dianteirodireito
        self.pneus_traseiroesquerdo = pneus_traseiroesquerdo
        self.pneus_traseirodireito = pneus_traseirodireito
        self.pneus_estepe = pneus_estepe
        self.higienizacao_externa = higienizacao_externa
        self.higienizacao_interna = higienizacao_interna
        self.cache_id = cache_id
        self.cache_field = cache_field
        self.cache_group = cache_group
        self.nome_falcao = nome_falcao

    def dadosAbertura(self):
        return('*Usuário:* ' + self.username.replace("_", " ") + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n\n' +
               '*Motivo de abertura:* ' + self.motivo + '\n' +
               '*Placa:* ' + self.placa + '\n' +
               '*KM Inicial:* ' + str(self.km_inicial) + '\n' +
               '*Manual está no veículo:* ' + strBool(self.manual) + '\n' +
               '*Chave reserva está no veículo:* ' + strBool(self.chave_reserva) + '\n').replace("_", " ").replace('[', " ").replace(']', " ")

    def dadosFechamento(self):
        return('*Usuário:* ' + self.username.replace("_", " ") + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n\n' +
               '*Motivo de fechamento:* ' + self.motivo + '\n' +
               '*Placa:* ' + self.placa + '\n' +
               '*KM Inicial:* ' + str(self.km_inicial) + '\n' +
               '*KM Final:* ' + str(self.km_final) + ' KM\n\n' +
               '*Manual está no veículo:* ' + strBool(self.manual) + '\n' +
               '*Chave reserva está no veículo:* ' + strBool(self.chave_reserva) + '\n' +
               '*Retornou com o carro para casa:* ' + strBool(self.carro_p_casa) + '\n' +
               '*Viajou com o carro:* ' + strBool(self.viajou_c_carro) + '\n' +
               '*Outro condutor:* ' + strBool(self.outro_condutor) + '\n' +
               '*Novo condutor:* ' + str(self.novo_condutor) + '\n' +
               '*Deixou na oficina:* ' + strBool(self.deixou_oficina) + '\n' +
               '*Local da oficina:* ' + str(self.local_oficina) + '\n' +
               '*Trocou o tacógrafo:* ' + strBool(self.van_tacografo) + '\n' +
               '*Calibrou os pneus:* ' + strBool(self.calibrou_pneu) + '\n').replace("_", " ").replace('[', " ").replace(']', " ")

    def dadosFalse(self):
        dict_data = self.__dict__

        dados = ''

        for key in dict_data:
            if (dict_data[key] == False):
                try:
                    a, b = key.split('_')
                    arr = ASSOC[a]
                    for tup in arr:
                        if b == tup[0]:
                            dados += 'O item: *' + tup[1] + '* não está ok\n'
                except:
                    continue
        
        return dados[:-1]



