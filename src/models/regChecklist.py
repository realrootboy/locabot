from datetime import datetime

class RegChecklist:
    
    def __init__(self,
                 username,
                 chat_id,
                 placa='',
                 km_inicial='',
                 dt_abertura=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                 km_final='',
                 dt_fechamento=None):
        self.username = username
        self.chat_id = chat_id
        self.placa = placa
        self.km_inicial = km_inicial
        self.dt_abertura = dt_abertura
        self.km_final = km_final
        self.dt_fechamento = dt_fechamento
