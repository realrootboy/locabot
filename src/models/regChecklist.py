from datetime import datetime


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


class RegChecklist:

    def __init__(self,
                 username,
                 chat_id,
                 placa='',
                 km_inicial='',
                 dt_abertura=datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00"),
                 km_final='',
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
                 mecanica_freiodemao=True
                 ):
        self.username = username
        self.chat_id = chat_id
        self.placa = placa
        self.km_inicial = km_inicial
        self.dt_abertura = dt_abertura
        self.km_final = km_final
        self.dt_fechamento = dt_fechamento
        self.id = idd
        self.motorista_id = motorista_id
        self.n_conformidades = 0
        self.media_dir = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ' ' + username
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

    def dadosAbertura(self):
        return('*Usuário:* ' + self.username + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n\n' +
               '*Placa:* ' + self.placa + '\n' +
               '*KM Inicial:* ' + str(self.km_inicial) + ' KM\n')

    def dadosFechamento(self):
        return('*Usuário:* ' + self.username + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n\n' +
               '*Placa:* ' + self.placa + '\n' +
               '*KM Inicial:* ' + str(self.km_inicial) + '\n'
               '*KM Final:* ' + str(self.km_final) + ' KM\n\n' +
               '*Retornou com o carro para casa:* ' + strBool(self.carro_p_casa) + '\n' +
               '*Viajou com o carro:* ' + strBool(self.viajou_c_carro) + '\n' +
               '*Outro condutor:* ' + strBool(self.outro_condutor) + '\n' +
               '*Novo condutor:* ' + str(self.novo_condutor) + '\n' +
               '*Deixou na oficina:* ' + strBool(self.deixou_oficina) + '\n' +
               '*Local da oficina:* ' + str(self.local_oficina) + '\n' +
               '*Trocou o tacógrafo:* ' + strBool(self.van_tacografo) + '\n' +
               '*Calibrou os pneus:* ' + strBool(self.calibrou_pneu) + '\n')

    def dadosMecanica(self):
        return('*CHECKLIST DE MECANICA*\n\n' +
               '*Motor:* ' + strBool2(self.mecanica_motor) + '\n'
               '*Amortecedor:* ' + strBool2(self.mecanica_amortecedor) + '\n'
               '*Escapamento:* ' + strBool2(self.mecanica_escapamento) + '\n'
               '*Freio:* ' + strBool2(self.mecanica_freio) + '\n'
               '*Embreagem:* ' + strBool2(self.mecanica_embreagem) + '\n'
               '*Acelerador:* ' + strBool2(self.mecanica_acelerador) + '\n'
               '*Cambio:* ' + strBool2(self.mecanica_cambio) + '\n'
               '*Oleo:* ' + strBool2(self.mecanica_oleo) + '\n'
               '*Agua:* ' + strBool2(self.mecanica_agua) + '\n'
               '*Alinhamento:* ' + strBool2(self.mecanica_alinhamento) + '\n'
               '*Freio de mão:* ' + strBool2(self.mecanica_freiodemao) + '\n')
