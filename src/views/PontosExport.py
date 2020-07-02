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

from datetime import datetime
from pytz import timezone

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
                PERIODO_ENVIO: [MessageHandler(Filters.text, self.periodo_envio)]
            },

            fallbacks=[CommandHandler('cancelar_info_ponto', self.cancel)]
        )

        self.disponiveis = CommandHandler('disponiveis', self.disponiveis)


    def disponiveis(self, update, context):
        disponiveis = '*DISPONIVEIS DO ADMINISTRATIVO*\n\n'

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
                    disponiveis += item.administrativo.nome + ' @' + item.administrativo.telegram_user +'\n'

        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        session.close()

        update.message.reply_text(disponiveis, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)



    def registro(self, update, context):
        if update.message.from_user.username is None:
            update.message.reply_text(
                'Não é possível realizar o cadastro de ponto sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

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

        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        update.message.reply_text(
            'Olá, ' + administrativo.nome + '. Por favor, escolha o setor de consulta.',
            reply_markup=ReplyKeyboardMarkup([['Administrativo'], ['Motorista'], ['Cancelar']], one_time_keyboard=True))

        session.close()

        return ESCOLHA_ROLE
    
    def escolha_role(self, update, context):
        if(update.message.text == 'Administrativo'):
            Session = Database.Session
            session = Session()

            adms_reply = []

            administrativos = session.query(Administrativo).order_by(Administrativo.nome.asc())

            for administrativo in administrativos:
                adms_reply.append([administrativo.nome + ' @' + administrativo.telegram_user])

            update.message.reply_text(
                'Por favor, informe o funcionário.',
                reply_markup=ReplyKeyboardMarkup(adms_reply, one_time_keyboard=True))

            session.close()

            return ESCOLHA_ADMINISTRATIVO
        elif(update.message.text == 'Motorista'):
            update.message.reply_text(
                'Ainda não implementado!',
                reply_markup=ReplyKeyboardRemove())

            return ConversationHandler.END
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            return ConversationHandler.END
        else:
            reply_keyboard2 = [['Administrativo'], ['Motorista'], ['Cancelar']]
            update.message.reply_text(
                'Opção inválida, por favor responda apenas: "Administrativo", "Motorista" ou "Cancelar".',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
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

        if (not (update.message.from_user.username == usuario_enviado)) and (not (update.message.from_user.username == 'igorpittol')):
            update.message.reply_text('Operação não permitida/Privilégios insuficientes.')

            return ConversationHandler.END

        administrativo = session.query(Administrativo).filter_by(
            telegram_user=usuario_enviado).first()

        if administrativo is None:
            Session = Database.Session
            session = Session()

            adms_reply = []

            administrativos = session.query(Administrativo).order_by(Administrativo.nome.asc())

            for administrativo in administrativos:
                adms_reply.append([administrativo.nome + ' @' + administrativo.telegram_user])

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
    
            periodos = CalendarUtils.periodosRange(min_date.month, min_date.year, max_date.month, max_date.year)
        except:
            update.message.reply_text('Não há registros.', reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        if not periodos:
            update.message.reply_text('Não há registros.', reply_markup=ReplyKeyboardRemove())
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
        update.message.reply_text('Selecione o período:', reply_markup=ReplyKeyboardMarkup(periodos, one_time_keyboard=True))

        return PERIODO_ENVIO


    def periodo_envio(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if not [update.message.text] in item.periodos:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Período inválido, por favor, informe novamente.')

            update.message.reply_text('Selecione o período:', reply_markup=ReplyKeyboardMarkup(item.periodos, one_time_keyboard=True))

            return PERIODO_ENVIO

        Session = Database.Session
        session = Session()

        administrativo = session.query(Administrativo).filter_by(
                        telegram_user=item.username_send).first()

        month, year = update.message.text.split(' ')
        
        range_intervalo = CalendarUtils.getRangeByFullMonth(month, year)

        adm_ponto = session.query(PontosAdministrativo).filter_by(
                administrativo_id=administrativo.id,
            ).filter(
                PontosAdministrativo.entrada >= range_intervalo[0],
                PontosAdministrativo.entrada <= range_intervalo[1],
                PontosAdministrativo.saida != None
            ).order_by(
                PontosAdministrativo.entrada.asc()
            )

        clock_ins = []

        for ponto in adm_ponto:
            item.acumulateHorasTrabalhadas(ponto.horas_trabalhadas)
            intervalos = session.query(IntervalosDePontoAdministrativo).filter_by(
                ponto=ponto)
            clock_ins.append(item.pontoToArrayFormatted(ponto, intervalos))

        factory = PdfFactory('media/' + item.media_dir )

        buff.pop(buff.index(item))

        fileToSend = factory.sheetHours(month, year, administrativo, clock_ins, item.horas_trabalhadas_send, 'N/A')
        context.bot.sendDocument(chat_id=item.chat_id, document=fileToSend)
       
        os.unlink(fileToSend.name)

        return ConversationHandler.END

    def escolha_motorista(self, update, context):
        return

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
