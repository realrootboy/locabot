from datetime import datetime
from pytz import timezone

class RegAbastecimento:

    def __init__(self,
                 username,
                 chat_id,
                 placa='',
                 quilometragem='',
                 qnt_litro='',
                 val_litro='',
                 val_total='',
                 tp_combustivel='',
                 posto=''):
        self.username = username
        self.chat_id = chat_id
        self.placa = placa
        self.quilometragem = quilometragem
        self.qnt_litro = qnt_litro
        self.val_litro = val_litro
        self.val_total = val_total
        self.tp_combustivel = tp_combustivel
        self.posto = posto
        self.media_dir = datetime.now(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y (%H:%M:%S.%f)') + ' ' + username

    def stringData(self):
        return('*Usuário:* ' + self.username + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n\n' +
               '*Placa:* ' + self.placa + '\n' +
               '*Quilometragem:* ' + str(self.quilometragem) + ' KM\n' +
               '*Quantidade de Litros:* ' + str(self.qnt_litro) + ' L\n' +
               '*Valor do Litro:* R$ ' + str(self.val_litro) + '\n' +
               '*Valor total:* R$ ' + str(self.val_total) + '\n' +
               '*Tipo de combustível:* ' + self.tp_combustivel + '\n' +
               '*Posto:* ' + self.posto)
