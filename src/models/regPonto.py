from datetime import datetime
from pytz import timezone

def tzToHumans(time):
    try:
        return time.astimezone(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y (%H:%M:%S)')
    except:
        return ''

class RegPonto:

    def getFilteredRole(self):
        if(self.role == 'motorista'):
            return self.role
        else:
            return self.specific_role

    

    def __init__(self,
                 username,
                 chat_id,
                 role='',
                 specific_role='',
                 entrada=None,
                 intervalo=None,
                 fim_intervalo=None,
                 saida=None):
        self.username = username
        self.chat_id = chat_id
        self.role = role
        self.specific_role = specific_role
        self.entrada = entrada
        self.intervalo = intervalo
        self.fim_intervalo = fim_intervalo
        self.saida = saida
    
    def stringData(self):
        return('*Usuário:* ' + self.username + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n' +
               '*Função:* ' + self.getFilteredRole() + '\n\n' +
               '*Entrada:* ' + tzToHumans(self.entrada) + '\n' +
               '*Intervalo:* ' + tzToHumans(self.intervalo) + '\n' +
               '*Fim do Intervalo:* ' + tzToHumans(self.fim_intervalo) + '\n' +
               '*Saida:* ' + tzToHumans(self.saida))
