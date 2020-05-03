from datetime import datetime

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
                 motorista_id=-1):
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

    def dadosAbertura(self):
        return('*Usuário:* ' + self.username + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n\n' +
               '*Placa:* ' + self.placa + '\n' +
               '*KM Inicial:* ' + str(self.km_inicial) + ' KM\n')
    
    def dadosFechamento(self):
        return('*Usuário:* ' + self.username + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n\n' +
               '*Placa:* ' + self.placa + '\n' +
               '*KM Inicial:* ' + str(self.km_inicial) +
               '*KM Final:* ' + str(self.km_final) + ' KM')
