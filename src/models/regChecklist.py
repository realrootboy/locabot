from datetime import datetime

def strBool(b):
    if(b):
        return 'Sim'
    else:
        return 'Não'

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
                 calibrou_pneu=False):
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
