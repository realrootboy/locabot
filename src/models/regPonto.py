from datetime import datetime
from pytz import timezone


def tzToHumans(time):
    try:
        return time.astimezone(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y (%H:%M:%S)')
    except:
        return ''


class RegPonto:

    def getFilteredRole(self):
        return self.role

    def intervalosToStr(self):
        if (self.intervalos is None) or (self.intervalos.count() == 0):
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
                 intervalos = None,
                 horas_trabalhadas = None):
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
        self.horas_trabalhadas = horas_trabalhadas

    def stringData(self):
        return('*Usuário:* ' + self.username + '\n' +
               '*Chat Atual:* ' + str(self.chat_id) + '\n' +
               '*Função:* ' + self.getFilteredRole() + '\n\n' +
               '*Entrada:* ' + tzToHumans(self.entrada) + '\n' +
               self.intervalosToStr() + '\n' +
               '*Saida:* ' + tzToHumans(self.saida) + 
               self.getHorasTrabalhadas())
    
    def getHorasTrabalhadas(self):
        if self.horas_trabalhadas:
            return ('\n\n========\n\n' + '*Horas Trabalhadas:* ' + self.horas_trabalhadas)
        return ''

    def calculateHours(self, intervalos=None):
        diff = self.saida - self.entrada
        seconds = diff.total_seconds()

        if intervalos:
            for index, item in enumerate(intervalos):
                print((item.fim_intervalo - item.intervalo).total_seconds())
                seconds -= (item.fim_intervalo - item.intervalo).total_seconds()

        seconds = seconds % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        self.horas_trabalhadas = "%d:%02d:%02d" % (hour, minutes, seconds) 
