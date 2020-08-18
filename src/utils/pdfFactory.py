from datetime import datetime
import os
from pytz import timezone
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import shutil

class PdfFactory:
    def __init__(self, filename='generated.pdf'):
        self.filename = filename

        self.doc = SimpleDocTemplate(filename,pagesize=letter,
                        rightMargin=16,leftMargin=16,
                        topMargin=16,bottomMargin=16)
        self.Story = []

    def falcao(self, motoristas_set):
        worksheet_title = 'HORARIOS DOS MOTORISTAS - FALCÃO BAUER'
        date_of_issue = 'Data de emissão: ' + datetime.now(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y (%H:%M:%S)')
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

        if motoristas_set is None:
            return None
        
        for motorista in motoristas_set:
            table_input = [
                    [motorista['nome']]
            ]
            table_input.append(['Dia', 'Entrada', 'Saida', 'Total Diário'])
            for dia in list(motorista['horarios']):
                
                for hrs in list(motorista['horarios'][dia]):
                    table_input.append([dia, hrs[0], hrs[1], hrs[2]])
                
            table_input.append(['Total Final', motorista['total_final']])
            
            t=Table(table_input, 130)
            t.setStyle(TableStyle([
                ('SPAN', (0,0), (3,0)),
                ('BOTTOMPADDING', (0,0), (0,0), 10),
                ('SIZE', (0,0), (0,0), 14),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
			    ('BOX', (0,0), (-1,-1), 0.25, colors.black)
            ]))

            self.Story.append(t)
            self.Story.append(Paragraph("<para alignment=right>-</para>" , styles["Normal"]))

        

        self.Story.append(Paragraph("<para alignment=right>%s</para>" % date_of_issue, styles["Normal"]))
        self.doc.build(self.Story)

        return open(self.filename, 'rb')

    def sheetHours(self, month=None, year=None, employee=None, clock_ins=None, worked = 0, extra = 0):
        worksheet_title = 'FOLHA DE PONTO MENSAL' + '(' + month + '/' + year + ')'
        date_of_issue = 'Data de emissão: ' + datetime.now(timezone('America/Sao_Paulo')).strftime('%d-%b-%Y (%H:%M:%S)')
        employer = 'Empregador ou CNPJ: '
        ###############
        if employee is None:
        	return None
        name = 'Nome: ' + employee.nome
        if employee.role:
            role = 'Função: ' + employee.role
        else:
            role = 'Função: motorista'
        
        cpf = 'CPF: '
        ctps = 'CTPS: '
        ###############
        total_worked = 'Horas Trabalhadas: ' + worked
        total_extra = 'Horas Extras: ' + extra
        totals = [total_worked, total_extra]
        ###############
        input_title = 'Entrada'
        intervals_title = 'Intervalos'
        output_title = 'Saida'
        day_hours_title = 'Horas Por Dia'
        clock_ins_titles = [input_title, intervals_title, output_title, day_hours_title]
        ###############
        table_input = [
            [worksheet_title],
            [employer],
            [name, '', role],
            [cpf, '', ctps],
            [total_worked, '', total_extra],
            [''],
            clock_ins_titles
        ]
        if clock_ins is None:
            return None
        for clock_in in clock_ins:
            table_input.append(clock_in)
        t=Table(table_input, 130)
        t.setStyle(TableStyle([
            ('ALIGN', (0,0), (0,0), 'CENTER'),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('SIZE', (0,0), (0,0), 16),
            ('BOTTOMPADDING', (0,0), (0,0), 10),
            ('SPAN', (0,0), (3,0)),
            ('SPAN', (0,1), (3,1)),
            ('SPAN', (0,2), (2,2)),
            ('SPAN', (2,2), (3,2)),
            ('SPAN', (0,3), (2,3)),
            ('SPAN', (2,3), (3,3)),
            ('SPAN', (0,4), (2,4)),
            ('SPAN', (2,4), (3,4)),
            ('SPAN', (0,5), (3,5)),
            ('ALIGN', (0,6), (3,6), 'CENTER'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black)
        ]))
        styles=getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        self.Story.append(t)
        self.Story.append(Paragraph("<para alignment=right>%s</para>" % date_of_issue, styles["Normal"]))
        self.doc.build(self.Story)
        return open(self.filename, 'rb')

# shutil.rmtree('media/' + item.media_dir , ignore_errors=True)
# document = open('PDF.pdf', 'rb')
# bot.sendDocument(chat_id=chat_id, document=document)
