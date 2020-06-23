from datetime import datetime
from pytz import timezone


def tzToHumans(time):
	try:
		return time.astimezone(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y (%H:%M:%S)')
	except:
		return ''

class RegPdfPonto:

	def __init__(self,
				 username,
				 chat_id,
				 role_send=None,
				 username_send=None,
				 name_send=None,
				 periodos=None):
		self.username = username
		self.chat_id = chat_id
		self.role_send = role_send
		self.username_send = username_send
		self.name_send = name_send
		self.periodos = periodos
		self.media_dir = datetime.now(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y') + ' ' + self.username_send + '.pdf'
		self.horas_trabalhadas_send = '00:00:00'

	def pontoToArrayFormatted(self, ponto, intervalos):
		return [tzToHumans(ponto.entrada), self.intervalosToStr(intervalos), tzToHumans(ponto.saida), ponto.horas_trabalhadas]

	def intervalosToStr(self, intervalos):
		if (intervalos is None) or (intervalos.count() == 0):
			return ''
        
		string = ''

		for index, item in enumerate(intervalos):
			string = (string + 'INTERVALO ' + str(index + 1) + '\n' + 
				tzToHumans(item.intervalo) + '\n' +
				tzToHumans(item.fim_intervalo) + '\n')

		return string[:-1]

	def acumulateHorasTrabalhadas(self, hour):
		hours, minutes, seconds = self.horas_trabalhadas_send.split(':')
		new_hours, new_minutes, new_seconds = hour.split(':')

		sum_seconds = int(seconds) + int(new_seconds)
		seconds = sum_seconds % 60

		sum_minutes = int(minutes) + int(new_minutes) + (sum_seconds // 60)
		minutes = sum_minutes % 60

		sum_hours = int(hours) + int(new_hours) + (sum_minutes // 60)
		hours = sum_hours

		self.horas_trabalhadas_send = str(hours) + ':' + str(minutes) + ':' + str(seconds)
