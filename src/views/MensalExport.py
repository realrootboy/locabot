from models.Administrativo import Administrativo

from models.Motorista import Motorista
from models.PontosMotorista import PontosMotorista
from models.IntervalosDePontoMotorista import IntervalosDePontoMotorista

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from database.main import Database
from sqlalchemy.sql import func

from utils import CalendarUtils
from utils.pdfFactory import PdfFactory
from utils.TimestampUtils import timestampToTimeTuple, datetimeArrToTimeTupleArr

from datetime import datetime
from pytz import timezone

import xlsxwriter
import shutil
import os


class MensalExport:
    def __init__(self, logger):
        self.logger = logger
        self.mensal = CommandHandler('ponto_mensal', self.mensal)

    def mensal(self, update, context):
        if update.message.from_user.username is None:
            update.message.reply_text(
                'Não é possível realizar a consulta sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return
        try:
            Session = Database.Session
            session = Session()

            administrativo = session.query(Administrativo).filter_by(
                telegram_user=update.message.from_user.username).first()

            if administrativo is None:
                update.message.reply_text(
                    'Usuário ' + update.message.from_user.username + ' não encontrado na base de dados. ' +
                    'Acesso não autorizado!', reply_markup=ReplyKeyboardRemove()
                )
                session.close()
                return
            session.close()
        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return

        if len(context.args) < 2:
            update.message.reply_text('Ola, ' + administrativo.nome + ' por favor, informe o mês e o ano ' +
                                      'da informação de mensal de ponto a ser consultada. \n\nEx: /ponto_mensal 10 2020')
            return

        try:
            month = int(context.args[0])
            year = int(context.args[1])
        except:
            update.message.reply_text('Os argumentos repassados devem ser números inteiros. \n\n' +
                                      'Ex: /ponto_mensal 10 2020')
            return
        
        if(month <= 0 or month > 12):
            update.message.reply_text('O mês informado é invalido.')
            return
    
        if(year < 2000 or year > 2100):
            update.message.reply_text('O ano informado é invalido.')
            return

        update.message.reply_text('Buscando e compilando registros...')

        local_path = 'media/PONTOS-' + \
                datetime.now(timezone('America/Sao_Paulo')
                             ).strftime('%b-%Y') + '.xlsx'

        workbook = xlsxwriter.Workbook(local_path)

        Session = Database.Session
        session = Session()

        motoristas = session.query(
                Motorista).order_by(Motorista.nome.asc())
        id_motorista = 0
        for motorista in motoristas:
            id_motorista = id_motorista + 1
            range_intervalo = CalendarUtils.getRangeByMonth(month, year)
            motorista_ponto = session.query(PontosMotorista).filter_by(
                motorista_id=motorista.id
            ).filter(
                PontosMotorista.entrada >= range_intervalo[0],
                PontosMotorista.entrada <= range_intervalo[1],
                PontosMotorista.saida != None
            ).order_by(
                PontosMotorista.entrada.asc()
            )

            pontos_dict = dict()
            for ponto in motorista_ponto:
                timetuple = timestampToTimeTuple(str(ponto.entrada))
                timetuple2 = timestampToTimeTuple(str(ponto.saida))
                intervalos = session.query(IntervalosDePontoMotorista).filter_by(
                    ponto=ponto)
                pontos_dict[timetuple[0]] = (timetuple[1],
                                             timetuple2[1],
                                             ponto.horas_trabalhadas,
                                             ponto.horas_extra,
                                             datetimeArrToTimeTupleArr)
            try:
                worksheet = workbook.add_worksheet(str(id_motorista) + " " +motorista.nome.split(" ")[0])
                row = 0
                col = 0
                worksheet.write(0, 0, "DATA")
                worksheet.write(0, 1, "ENTRADA")
                worksheet.write(0, 2, "SAIDA")
                worksheet.write(0, 3, "HORAS TRABALHADAS")
                worksheet.write(0, 4, "HORAS EXTRA")
                last_day = int(CalendarUtils.getLastDayMonth(CalendarUtils.REV_FULL_MONTHS[month], year))
                print('Last Day: ' + str(last_day))
                days = 20
                for i in range(last_day):
                    if(days == last_day):
                        days = 1
                    else:
                        days = days + 1
                    dia = str('%.2d' % (days)) + '/' + str('%.2d' % (month)) + '/' + str(year)
                    worksheet.write(row + i + 1, col, dia)
                    if dia in pontos_dict:
                        x = pontos_dict[dia]
                        worksheet.write(row + i + 1, 1, x[0])
                        worksheet.write(row + i + 1, 2, x[1])
                        worksheet.write(row + i + 1, 3, x[2])
                        worksheet.write(row + i + 1, 4, x[3])
                
            except Exception as e:
                print(e)
        session.close()
        workbook.close()

        planilha = open(local_path, 'rb')
        context.bot.sendDocument(chat_id=update.effective_chat.id, document=planilha)
        #os.remove(local_path)


