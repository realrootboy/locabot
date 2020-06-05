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

    def intervalosToStr(self):
        if self.intervalos is None:
            return ''
        
        string = '\n'
        for index, item in enumerate(self.intervalos):
            string = (string + 'INTERVALO ' + str(index + 1) + '\n' + 
                '*Inicio do intervalo:* ' + tzToHumans(item.intervalo) + '\n' +
                '*Fim do intervalo:* ' + tzToHumans(item.fim_intervalo) + '\n')
        
        return string

    def __init__(self,
                 username,
                 chat_id,
                 role='',
                 specific_role='',
                 entrada=None,
                 intervalo=None,
                 fim_intervalo=None,
                 saida=None,
                 id=-1,
                 intervalos = None):
        self.username = username
        self.chat_id = chat_id
        self.role = role
        self.specific_role = specific_role
        self.entrada = entrada
        self.intervalo = intervalo
        self.fim_intervalo = fim_intervalo
        self.saida = saida
        self.id = id
        self.intervalos = None

    def stringData(self):
        return('*Usuário:* ' + self.username + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n' +
               '*Função:* ' + self.getFilteredRole() + '\n\n' +
               '*Entrada:* ' + tzToHumans(self.entrada) + '\n' +
               self.intervalosToStr() + '\n' +
               '*Saida:* ' + tzToHumans(self.saida))
