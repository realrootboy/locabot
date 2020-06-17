from datetime import datetime
from pytz import timezone

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class PdfFactory:
	def __init__(self, filename='generated.pdf'):
		self.filename = filename

		self.doc = SimpleDocTemplate(filename,pagesize=letter,
                        rightMargin=16,leftMargin=16,
                        topMargin=16,bottomMargin=16)
		self.Story = []

	def sheetHours(self, month=None, year=None, employee=None, clock_ins=None, intervals=None):
		worksheet_title = 'FOLHA DE PONTO MENSAL'
		date_of_issue = 'Data de emissão: ' + datetime.now(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y (%H:%M:%S)')
		employer = 'Empregador ou CNPJ: '
		###############
		name = 'Nome: '
		role = 'Função: '
		cpf = 'CPF: RENAN MOREIRA GOMES'
		ctps = 'CTPS: 64651654654'

		
		###############
		total_worked = 'Horas Trabalhadas: '
		total_extra = 'Horas Extras: '
		
		totals = [total_worked, total_extra]
		###############
		day_title = 'Dia'
		input_title = 'Entrada'
		output_title = 'Saida'
		day_hours_title = 'Horas Regulares'

		clock_ins_data = [day_title, input_title, output_title, day_hours_title]
		###############

		table_input = [
			[worksheet_title],
			[employer],
			[name, '', role],
			[cpf, '', ctps],
			[total_worked, '', total_extra],
			[''],
			clock_ins_data
		]


		t=Table(table_input, 120)
		t.setStyle(TableStyle([
			('SPAN', (0,0), (3,0)),
			('SPAN', (0,1), (3,1)),
			('SPAN', (0,2), (2,2)),
			('SPAN', (2,2), (3,2)),
			('SPAN', (0,3), (2,3)),
			('SPAN', (2,3), (3,3)),
			('SPAN', (0,4), (2,4)),
			('SPAN', (2,4), (3,4)),
			('SPAN', (0,5), (3,5)),
			('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
			('BOX', (0,0), (-1,-1), 0.25, colors.black)
		]))

		self.Story.append(t)
		self.doc.build(self.Story)


fac = PdfFactory()
fac.sheetHours()



