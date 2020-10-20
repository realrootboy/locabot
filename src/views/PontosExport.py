from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from controllers.controllerUtils import listUtils

from models.Motorista import Motorista
from models.PontosMotorista import PontosMotorista
from models.IntervalosDePontoMotorista import IntervalosDePontoMotorista
from models.Administrativo import Administrativo
from models.PontosAdministrativo import PontosAdministrativo
from models.IntervalosDePontoAdministrativo import IntervalosDePontoAdministrativo

from models.regPdfPonto import RegPdfPonto

from database.main import Database
from sqlalchemy.sql import func

from utils import CalendarUtils
from utils.pdfFactory import PdfFactory
from utils.TimestampUtils import timestampToTimeTuple, datetimeArrToTimeTupleArr

from views.FalcaoBauer import getMotoristasSet

from datetime import datetime
from pytz import timezone

import xlsxwriter
import shutil
import os

buff = list()

ESCOLHA_ROLE = 1
ESCOLHA_ADMINISTRATIVO = 2
ESCOLHA_MOTORISTA = 3
PERIODO_ENVIO = 4


class PontosExport:
    def __init__(self, logger):
        self.logger = logger
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('info_ponto', self.registro)],

            states={
                ESCOLHA_ROLE: [MessageHandler(Filters.text, self.escolha_role)],
                ESCOLHA_ADMINISTRATIVO: [MessageHandler(Filters.text, self.escolha_administrativo)],
                ESCOLHA_MOTORISTA: [MessageHandler(Filters.text, self.escolha_motorista)],
                PERIODO_ENVIO: [MessageHandler(
                    Filters.text, self.periodo_envio)]
            },

            fallbacks=[CommandHandler('cancelar_info_ponto', self.cancel)]
        )

        self.disponiveis = CommandHandler('disponiveis', self.disponiveis)
        self.falcao = CommandHandler('falcao_bauer', self.falcao_bauer)

    def falcao_bauer(self, update, context):
        factory = PdfFactory('falcao.pdf')

        print(getMotoristasSet())

        fileToSend = factory.falcao(getMotoristasSet())

        context.bot.sendDocument(
            chat_id=update.message.chat_id, document=fileToSend)

        os.unlink(fileToSend.name)

        return

    def disponiveis(self, update, context):
        disponiveis = 'DISPONIVEIS DO ADMINISTRATIVO\n\n'

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
                return ConversationHandler.END

            adm_disponiveis = session.query(PontosAdministrativo).filter_by(
                saida=None)

            for item in adm_disponiveis:
                intervalo = session.query(IntervalosDePontoAdministrativo).filter_by(
                    ponto=item, fim_intervalo=None).order_by(IntervalosDePontoAdministrativo.id.desc()).first()
                if intervalo is None:
                    disponiveis += item.administrativo.nome + ' @' + \
                        item.administrativo.telegram_user + '\n'

        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        session.close()

        update.message.reply_text(
            disponiveis, reply_markup=ReplyKeyboardRemove())

    def registro(self, update, context):
        if update.message.from_user.username is None:
            update.message.reply_text(
                'Não é possível realizar a visualização de informações de ponto sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        try:
            Session = Database.Session
            session = Session()

            administrativo = session.query(Administrativo).filter_by(
                telegram_user=update.message.from_user.username).first()

            motorista = session.query(Motorista).filter_by(
                telegram_user=update.message.from_user.username).first()

            if (administrativo is None) and (motorista is None):
                update.message.reply_text(
                    'Usuário ' + update.message.from_user.username + ' não encontrado na base de dados. ' +
                    'Acesso não autorizado!', reply_markup=ReplyKeyboardRemove()
                )
                session.close()
                return ConversationHandler.END

        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        if administrativo:
            update.message.reply_text(
                'Olá, ' + administrativo.nome + '. Por favor, escolha o setor de consulta.',
                reply_markup=ReplyKeyboardMarkup([['Administrativo'], ['Motorista'], ['Cancelar']], one_time_keyboard=True))
        else:
            update.message.reply_text(
                'Olá, ' + motorista.nome + '. Por favor, escolha o setor de consulta.',
                reply_markup=ReplyKeyboardMarkup([['Administrativo'], ['Motorista'], ['Cancelar']], one_time_keyboard=True))

        session.close()

        return ESCOLHA_ROLE

    def escolha_role(self, update, context):
        if(update.message.text == 'Administrativo'):
            Session = Database.Session
            session = Session()

            adms_reply = []

            administrativos = session.query(
                Administrativo).order_by(Administrativo.nome.asc())

            for administrativo in administrativos:
                adms_reply.append(
                    [administrativo.nome + ' @' + administrativo.telegram_user])

            update.message.reply_text(
                'Por favor, informe o funcionário.',
                reply_markup=ReplyKeyboardMarkup(adms_reply, one_time_keyboard=True))

            session.close()

            return ESCOLHA_ADMINISTRATIVO
        elif(update.message.text == 'Motorista'):
            Session = Database.Session
            session = Session()
#
            motoristas_reply = []
#
            motoristas = session.query(
                Motorista).order_by(Motorista.nome.asc())
#
            for motorista in motoristas:
                motoristas_reply.append(
                    [motorista.nome + ' @' + motorista.telegram_user])
#
            update.message.reply_text(
                'Por favor, informe o motorista!',
                reply_markup=ReplyKeyboardMarkup(motoristas_reply, one_time_keyboard=True))
#
            return ESCOLHA_MOTORISTA
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            return ConversationHandler.END
        else:
            reply_keyboard2 = [['Administrativo'], ['Motorista'], ['Cancelar']]
            update.message.reply_text(
                'Opção inválida, por favor responda apenas: "Administrativo", "Motorista" ou "Cancelar".',
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard2, one_time_keyboard=True)
            )

        return

    def escolha_administrativo(self, update, context):
        user = update.message.from_user

        Session = Database.Session
        session = Session()

        try:
            nome, usuario_enviado = update.message.text.split(' @')
            if usuario_enviado == '':
                update.message.reply_text('Usuário não cadastrado, conversa encerrada.',
                                          reply_markup=ReplyKeyboardRemove())

                return ConversationHandler.END
        except:
            nome, usuario_enviado = ['xxx', 'xxx']

        if (
            (not (update.message.from_user.username == usuario_enviado))
            and (not (update.message.from_user.username == 'igorpittol'))
            and (not (update.message.from_user.username == 'stephanypsantos'))
            and (not (update.message.from_user.username == 'renanmgomes'))
        ):
            update.message.reply_text(
                'Operação não permitida/Privilégios insuficientes.')

            return ConversationHandler.END

        administrativo = session.query(Administrativo).filter_by(
            telegram_user=usuario_enviado).first()

        if administrativo is None:
            Session = Database.Session
            session = Session()

            adms_reply = []

            administrativos = session.query(
                Administrativo).order_by(Administrativo.nome.asc())

            for administrativo in administrativos:
                adms_reply.append(
                    [administrativo.nome + ' @' + administrativo.telegram_user])

            update.message.reply_text(
                'Funcionário ' + update.message.text + ' inválido ou não encontrado na base de dados. ' +
                'Por favor, informe novamente o funcionário.',
                reply_markup=ReplyKeyboardMarkup(adms_reply, one_time_keyboard=True))

            session.close()

            return ESCOLHA_ADMINISTRATIVO

        # buff.append(pdfPonto)

        administrativo = session.query(Administrativo).filter_by(
            telegram_user=usuario_enviado).first()

        adm_intervalo = session.query(
            func.min(PontosAdministrativo.entrada).label("min_date"),
            func.max(PontosAdministrativo.saida).label("max_date")).filter_by(
                administrativo_id=administrativo.id
        )
        try:
            res = adm_intervalo.one()
            min_date = res.min_date
            max_date = res.max_date

            periodos = CalendarUtils.periodosRange(
                min_date.month, min_date.year, max_date.month, max_date.year)
        except:
            update.message.reply_text(
                'Não há registros.', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        if not periodos:
            update.message.reply_text(
                'Não há registros.', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        pdfPonto = RegPdfPonto(
            username=update.message.from_user.username,
            chat_id=update.message.chat_id,
            role_send='administrativo',
            username_send=usuario_enviado,
            name_send=nome,
            periodos=periodos
        )

        buff.append(pdfPonto)

        session.close()
        update.message.reply_text('Selecione o período:', reply_markup=ReplyKeyboardMarkup(
            periodos, one_time_keyboard=True))

        return PERIODO_ENVIO

    def periodo_envio(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if not [update.message.text] in item.periodos:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Período inválido, por favor, informe novamente.')

            update.message.reply_text('Selecione o período:', reply_markup=ReplyKeyboardMarkup(
                item.periodos, one_time_keyboard=True))

            return PERIODO_ENVIO

        Session = Database.Session
        session = Session()

        if item.role_send == 'administrativo':
            administrativo = session.query(Administrativo).filter_by(
                telegram_user=item.username_send).first()

            month, year = update.message.text.split(' ')

            range_intervalo = CalendarUtils.getRangeByFullMonth(month, year)

            adm_ponto = session.query(PontosAdministrativo).filter_by(
                administrativo_id=administrativo.id
            ).filter(
                PontosAdministrativo.entrada >= range_intervalo[0],
                PontosAdministrativo.entrada <= range_intervalo[1],
                PontosAdministrativo.saida != None
            ).order_by(
                PontosAdministrativo.entrada.asc()
            )

            clock_ins = []
            local_path = 'media/PONTOS-' + \
                datetime.now(timezone('America/Sao_Paulo')
                             ).strftime('%b-%Y') + '.xlsx'

            model_to_impress = administrativo

            pontos_dict = dict()
            for ponto in adm_ponto:
                item.acumulateHorasTrabalhadas(ponto.horas_trabalhadas)
                timetuple = timestampToTimeTuple(str(ponto.entrada))
                timetuple2 = timestampToTimeTuple(str(ponto.saida))
                intervalos = session.query(IntervalosDePontoAdministrativo).filter_by(
                    ponto=ponto)
                pontos_dict[timetuple[0]] = (timetuple[1],
                                             timetuple2[1],
                                             ponto.horas_trabalhadas,
                                             ponto.horas_extra,
                                             datetimeArrToTimeTupleArr)
                clock_ins.append(item.pontoToArrayFormatted(ponto, intervalos))

            try:
                workbook = xlsxwriter.Workbook(local_path)
                worksheet = workbook.add_worksheet()
                row = 0
                col = 0

                worksheet.write(0, 0, "DATA")
                worksheet.write(0, 1, "ENTRADA")
                worksheet.write(0, 2, "SAIDA")
                worksheet.write(0, 3, "HORAS TRABALHADAS")
                worksheet.write(0, 4, "HORAS EXTRA")

                for i in range(CalendarUtils.getLastDayMonth(month, year)):
                    dia = str('%.2d' % (i+1) + '/' + '%.2d' %
                              CalendarUtils.FULL_MONTHS[month] + '/' + year)
                    worksheet.write(row + i + 1, col, dia)
                    if dia in pontos_dict:
                        x = pontos_dict[dia]
                        worksheet.write(row + i + 1, 1, x[0])
                        worksheet.write(row + i + 1, 2, x[1])
                        worksheet.write(row + i + 1, 3, x[2])
                        worksheet.write(row + i + 1, 4, x[3])

                workbook.close()
            except Exception as e:
                print(e)
                os.remove(local_path)

        elif item.role_send == 'motorista':
            motorista = session.query(Motorista).filter_by(
                telegram_user=item.username_send).first()

            month, year = update.message.text.split(' ')

            range_intervalo = CalendarUtils.getRangeByFullMonth(month, year)

            motorista_ponto = session.query(PontosMotorista).filter_by(
                motorista_id=motorista.id
            ).filter(
                PontosMotorista.entrada >= range_intervalo[0],
                PontosMotorista.entrada <= range_intervalo[1],
                PontosMotorista.saida != None
            ).order_by(
                PontosMotorista.entrada.asc()
            )

            clock_ins = []

            for ponto in motorista_ponto:
                item.acumulateHorasTrabalhadas(ponto.horas_trabalhadas)
                intervalos = session.query(
                    IntervalosDePontoMotorista).filter_by(ponto=ponto)
                clock_ins.append(item.pontoToArrayFormatted(ponto, intervalos))

            model_to_impress = motorista

            local_path = 'media/PONTOS-' + \
                datetime.now(timezone('America/Sao_Paulo')
                             ).strftime('%b-%Y') + '.xlsx'

            pontos_dict = dict()
            for ponto in adm_ponto:
                item.acumulateHorasTrabalhadas(ponto.horas_trabalhadas)
                timetuple = timestampToTimeTuple(str(ponto.entrada))
                timetuple2 = timestampToTimeTuple(str(ponto.saida))
                intervalos = session.query(IntervalosDePontoAdministrativo).filter_by(
                    ponto=ponto)
                pontos_dict[timetuple[0]] = (timetuple[1],
                                             timetuple2[1],
                                             ponto.horas_trabalhadas,
                                             ponto.horas_extra,
                                             datetimeArrToTimeTupleArr)
                clock_ins.append(item.pontoToArrayFormatted(ponto, intervalos))

            try:
                workbook = xlsxwriter.Workbook(local_path)
                worksheet = workbook.add_worksheet()
                row = 0
                col = 0

                worksheet.write(0, 0, "DATA")
                worksheet.write(0, 1, "ENTRADA")
                worksheet.write(0, 2, "SAIDA")
                worksheet.write(0, 3, "HORAS TRABALHADAS")
                worksheet.write(0, 4, "HORAS EXTRA")

                for i in range(CalendarUtils.getLastDayMonth(month, year)):
                    dia = str('%.2d' % (i+1) + '/' + '%.2d' %
                              CalendarUtils.FULL_MONTHS[month] + '/' + year)
                    worksheet.write(row + i + 1, col, dia)
                    if dia in pontos_dict:
                        x = pontos_dict[dia]
                        worksheet.write(row + i + 1, 1, x[0])
                        worksheet.write(row + i + 1, 2, x[1])
                        worksheet.write(row + i + 1, 3, x[2])
                        worksheet.write(row + i + 1, 4, x[3])

                workbook.close()
            except Exception as e:
                print(e)
                os.remove(local_path)

        factory = PdfFactory('media/' + item.media_dir)

        buff.pop(buff.index(item))

        fileToSend = factory.sheetHours(
            month, year, model_to_impress, clock_ins, item.horas_trabalhadas_send, 'N/A')
        context.bot.sendDocument(chat_id=item.chat_id, document=fileToSend)

        if item.role_send == 'administrativo':
            planilha = open(local_path, 'rb')
            context.bot.sendDocument(chat_id=item.chat_id, document=planilha)

        os.unlink(fileToSend.name)

        return ConversationHandler.END

    def escolha_motorista(self, update, context):
        user = update.message.from_user

        Session = Database.Session
        session = Session()

        try:
            nome, usuario_enviado = update.message.text.split(' @')
            if usuario_enviado == '':
                update.message.reply_text('Usuário não cadastrado, conversa encerrada.',
                                          reply_markup=ReplyKeyboardRemove())

                return ConversationHandler.END
        except:
            nome, usuario_enviado = ['xxx', 'xxx']

        if (
            (not (update.message.from_user.username == usuario_enviado))
            and (not (update.message.from_user.username == 'igorpittol'))
            and (not (update.message.from_user.username == 'stephanypsantos'))
            and (not (update.message.from_user.username == 'renanmgomes'))
        ):
            update.message.reply_text(
                'Operação não permitida/Privilégios insuficientes.')

            return ConversationHandler.END

        motorista = session.query(Motorista).filter_by(
            telegram_user=usuario_enviado).first()

        if motorista is None:
            Session = Database.Session
            session = Session()

            motoristas_reply = []

            motoristas = session.query(
                Motorista).order_by(Motorista.nome.asc())

            for motorista in motoristas:
                motoristas_reply.append(
                    [motorista.nome + ' @' + motorista.telegram_user])

            update.message.reply_text(
                'Motorista ' + update.message.text + ' inválido ou não encontrado na base de dados. ' +
                'Por favor, informe novamente o motorista.',
                reply_markup=ReplyKeyboardMarkup(motoristas_reply, one_time_keyboard=True))

            session.close()

            return ESCOLHA_MOTORISTA

        # buff.append(pdfPonto)

        motorista = session.query(Motorista).filter_by(
            telegram_user=usuario_enviado).first()

        motorista_intervalo = session.query(
            func.min(PontosMotorista.entrada).label("min_date"),
            func.max(PontosAdministrativo.saida).label("max_date")).filter_by(
                motorista_id=motorista.id
        )
        try:
            res = motorista_intervalo.one()
            min_date = res.min_date
            max_date = res.max_date

            periodos = CalendarUtils.periodosRange(
                min_date.month, min_date.year, max_date.month, max_date.year)
        except:
            update.message.reply_text(
                'Não há registros.', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        if not periodos:
            update.message.reply_text(
                'Não há registros.', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        pdfPonto = RegPdfPonto(
            username=update.message.from_user.username,
            chat_id=update.message.chat_id,
            role_send='motorista',
            username_send=usuario_enviado,
            name_send=nome,
            periodos=periodos
        )

        buff.append(pdfPonto)

        session.close()
        update.message.reply_text('Selecione o período:', reply_markup=ReplyKeyboardMarkup(
            periodos, one_time_keyboard=True))

        return PERIODO_ENVIO

    def cancel(self, update, context):
        user = update.message.from_user
        self.logger.info("Usuario %s cancelou a conversa.", user.first_name)
        update.message.reply_text('Tchau!',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

# CONTROLE DE ACESSO ADMINISTRATIVO
# LISTAGEM DOS MOTORISTAS
# HORAS TRABALHADAS POR MES DO MOTORISTA
# import datetime
# import calendar
#
# year = 2012
# month = 6
#
# num_days = calendar.monthrange(year, month)[1]
# start_date = datetime.date(year, month, 1)
# end_date = datetime.date(year, month, num_days)
#
# results = session.query(Event).filter(
#     and_(Event.date >= start_date, Event.date <= end_date)).all()
