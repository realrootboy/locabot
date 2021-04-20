from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from datetime import datetime
from pytz import timezone

from controllers.controllerUtils import listUtils

from models.Motorista import Motorista
from models.Administrativo import Administrativo
from models.PontosMotorista import PontosMotorista
from models.PontosAdministrativo import PontosAdministrativo
from models.IntervalosDePontoMotorista import IntervalosDePontoMotorista
from models.IntervalosDePontoAdministrativo import IntervalosDePontoAdministrativo
from models.EscalasMotorista import EscalasMotorista

from models.regPonto import RegPonto

from utils import textLogger

from database.main import Database

OPTS, ENTRADA, INTERVALO, FIM_INTERVALO, SAIDA, REABERTURA = range(6)
buff = list()


def handleOpts(ponto):
    if(ponto.already):
        return [['Reabrir expediente']]
    if(ponto.entrada is None):
        return [['Abrir expediente']]
    elif(ponto.intervalo is None):
        return [['Iniciar intervalo'], ['Fechar expediente']]
    elif(ponto.fim_intervalo is None):
        return [['Fechar intervalo']]
    else:
        return [['Fechar expediente']]


class PontoController:

    def __init__(self, logger):
        self.logger = logger
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('bater_ponto', self.registro)],

            states={
                OPTS: [MessageHandler(Filters.text & (~ Filters.command), self.opts)],
                ENTRADA: [MessageHandler(Filters.text & (~ Filters.command), self.entrada)],
                INTERVALO: [MessageHandler(Filters.text & (~ Filters.command), self.intervalo)],
                FIM_INTERVALO: [MessageHandler(Filters.text & (~ Filters.command), self.fim_intervalo)],
                SAIDA: [MessageHandler(Filters.text & (~ Filters.command), self.saida)],
                REABERTURA: [MessageHandler(Filters.text & (~ Filters.command), self.reabertura)]
            },

            fallbacks=[CommandHandler('cancelar', self.cancel)]
        )

    def registro(self, update, context):
        # VALIDAÇÃO DE NOME DE USUARIO DO TELEGRAM
        try:
            ponto = RegPonto(
                username=update.message.from_user.username,
                chat_id=update.message.chat.id
            )
        except Exception as e:
            print(e)
            update.message.reply_text(
                'Não é possível realizar o cadastro de ponto sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        if update.message.from_user.username is None:
            update.message.reply_text(
                'Não é possível realizar o cadastro de ponto sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
        # =========================================

        try:
            Session = Database.Session
            session = Session()

            administrativo = session.query(Administrativo).filter_by(
                telegram_user=ponto.username
            ).first()

            if administrativo is None:
                motorista = session.query(Motorista).filter_by(
                    telegram_user=ponto.username
                ).first()

                if motorista is None:
                    session.close()
                    return ConversationHandler.END
                else:
                    pontoDb = session.query(PontosMotorista).filter_by(
                        motorista_id=motorista.id).order_by(PontosMotorista.entrada.desc()).first()
                    ponto.role = 'motorista'
                    nome = motorista.nome
            else:
                pontoDb = session.query(PontosAdministrativo).filter_by(
                    administrativo_id=administrativo.id).order_by(PontosAdministrativo.entrada.desc()).first()
                ponto.role = administrativo.role
                nome = administrativo.nome
            
            if (pontoDb and pontoDb.saida is None):
                ponto.entrada = pontoDb.entrada
                ponto.saida = pontoDb.saida
                ponto.id = pontoDb.id
                ponto.already = False
            elif (pontoDb and pontoDb.saida) and (pontoDb.entrada.day == datetime.now(timezone('America/Sao_Paulo')).day):
                ponto.entrada = pontoDb.entrada
                ponto.saida = pontoDb.saida
                ponto.id = pontoDb.id
                ponto.already = True

        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        try:
            if ponto.role == 'motorista':
                intervaloDePonto = session.query(IntervalosDePontoMotorista).filter_by(
                    ponto_motorista_id=pontoDb.id).order_by(IntervalosDePontoMotorista.intervalo.desc()).first()
            else:
                intervaloDePonto = session.query(IntervalosDePontoAdministrativo).filter_by(
                    ponto_administrativo_id=pontoDb.id).order_by(IntervalosDePontoAdministrativo.intervalo.desc()).first()
            if (intervaloDePonto and intervaloDePonto.fim_intervalo is None):
                ponto.intervalo = intervaloDePonto.intervalo
                ponto.fim_intervalo = intervaloDePonto.fim_intervalo
        except Exception as e:
            print(e)

        session.close()

        replyKeyboard = handleOpts(ponto)


        buff.append(ponto)

        update.message.reply_text(
            'Olá, ' + nome + '. Por favor, escolha a opção desejada.',
            reply_markup=ReplyKeyboardMarkup(
                replyKeyboard, one_time_keyboard=True)
        )

        return OPTS

    def opts(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Abrir expediente'):
            update.message.reply_text(
                'Deseja confirmar a abertura de expediente?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return ENTRADA
        elif(update.message.text == 'Iniciar intervalo'):
            update.message.reply_text(
                'Deseja confirmar a abertura de intervalo?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return INTERVALO
        elif(update.message.text == 'Fechar intervalo'):
            update.message.reply_text(
                'Deseja confirmar o fechamento de intervalo?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return FIM_INTERVALO
        elif(update.message.text == 'Fechar expediente'):
            update.message.reply_text(
                'Deseja confirmar o fechamento de expediente?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return SAIDA
        elif(update.message.text == 'Reabrir expediente'):
            update.message.reply_text(
                'Deseja confirmar a reabertura de expediente?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return REABERTURA
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas com: ' +
                str(handleOpts(item)).replace('[', '').replace(']', ''))

            update.message.reply_text(
                'Olá. Por favor, escolha a opção desejada.',
                reply_markup=ReplyKeyboardMarkup(
                    handleOpts(item), one_time_keyboard=True)
            )

            return OPTS

    def entrada(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'entrada',
                                      datetime.now(timezone('America/Sao_Paulo')).replace(second=0, microsecond=0))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                if(item.role == 'motorista'):
                    motorista = session.query(Motorista).filter_by(
                        telegram_user=item.username).first()

                
                    ponto = PontosMotorista(
                        motorista,
                        item.entrada,
                        item.saida
                    )
                
                else:
                    administrativo = session.query(Administrativo).filter_by(
                        telegram_user=item.username).first()
                    
                    ponto = PontosAdministrativo(
                        administrativo,
                        item.entrada,
                        item.saida
                    )

                session.add(ponto)

                session.commit()
                session.close()
            except Exception as e:
                update.message.reply_text('Houve um erro ao tentar salvar! ' +
                                          'O erro foi reportado, tente novamente mais tarde.',
                                          reply_markup=ReplyKeyboardRemove())
                print(e)
                buff.pop(buff.index(item))
                return ConversationHandler.END

            buff.pop(buff.index(item))

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=item.stringData(),
                parse_mode=ParseMode.MARKDOWN
            )

            return ConversationHandler.END
        elif(update.message.text == 'Não, finalizar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!',
                reply_markup=ReplyKeyboardRemove())

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas com: ' +
                '"Sim, confirmar" ou "Não, finalizar"')

            update.message.reply_text(
                'Deseja confirmar a abertura de expediente?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return ENTRADA

    def intervalo(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'intervalo',
                                      datetime.now(timezone('America/Sao_Paulo')).replace(second=0, microsecond=0))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                if item.role == 'motorista':
                    motorista = session.query(Motorista).filter_by(
                        telegram_user=item.username).first()

                    pontoDb = session.query(PontosMotorista).filter_by(
                        motorista_id=motorista.id).order_by(PontosMotorista.entrada.desc()).first()

                    intervalo = IntervalosDePontoMotorista(
                        pontoDb,
                        item.intervalo,
                        item.fim_intervalo
                    )
                else:
                    administrativo = session.query(Administrativo).filter_by(
                        telegram_user=item.username).first()
                    
                    pontoDb = session.query(PontosAdministrativo).filter_by(
                        administrativo_id=administrativo.id).order_by(PontosAdministrativo.entrada.desc()).first()
                    
                    intervalo = IntervalosDePontoAdministrativo(
                        pontoDb,
                        item.intervalo,
                        item.fim_intervalo
                    )

                session.add(intervalo)
                session.commit()

                if item.role == 'motorista':
                    intervalos = session.query(IntervalosDePontoMotorista).filter_by(
                        ponto_motorista_id=pontoDb.id)
                else:
                    intervalos = session.query(IntervalosDePontoAdministrativo).filter_by(
                        ponto_administrativo_id=pontoDb.id)
                
                item.intervalos = intervalos

                session.close()
            except Exception as e:
                update.message.reply_text('Houve um erro ao tentar salvar! ' +
                                          'O erro foi reportado, tente novamente mais tarde.',
                                          reply_markup=ReplyKeyboardRemove())
                print(e)
                buff.pop(buff.index(item))
                return ConversationHandler.END

            buff.pop(buff.index(item))

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=item.stringData(),
                parse_mode=ParseMode.MARKDOWN
            )

            return ConversationHandler.END
        elif(update.message.text == 'Não, finalizar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!',
                reply_markup=ReplyKeyboardRemove())

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas com: ' +
                '"Sim, confirmar" ou "Não, finalizar"')

            update.message.reply_text(
                'Deseja confirmar a abertura de intervalo?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return INTERVALO

    def fim_intervalo(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'fim_intervalo',
                                      datetime.now(timezone('America/Sao_Paulo')).replace(second=0, microsecond=0))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                if item.role == 'motorista':
                    motorista = session.query(Motorista).filter_by(
                        telegram_user=item.username).first()

                    pontoDb = session.query(PontosMotorista).filter_by(
                        motorista_id=motorista.id).order_by(PontosMotorista.entrada.desc()).first()

                    intervalo = session.query(IntervalosDePontoMotorista).filter_by(
                        ponto_motorista_id=pontoDb.id).order_by(IntervalosDePontoMotorista.intervalo.desc()).first()
                else:
                    administrativo = session.query(Administrativo).filter_by(
                        telegram_user=item.username).first()
                    
                    pontoDb = session.query(PontosAdministrativo).filter_by(
                        administrativo_id=administrativo.id).order_by(PontosAdministrativo.entrada.desc()).first()
                    
                    intervalo = session.query(IntervalosDePontoAdministrativo).filter_by(
                        ponto_administrativo_id=pontoDb.id).order_by(IntervalosDePontoAdministrativo.intervalo.desc()).first()

                intervalo.fim_intervalo = item.fim_intervalo

                session.add(intervalo)

                session.commit()

                if item.role == 'motorista':
                    intervalos = session.query(IntervalosDePontoMotorista).filter_by(
                        ponto_motorista_id=pontoDb.id)
                else:
                    intervalos = session.query(IntervalosDePontoAdministrativo).filter_by(
                        ponto_administrativo_id=pontoDb.id)
                
                item.intervalos = intervalos

                session.close()
            except Exception as e:
                update.message.reply_text('Houve um erro ao tentar salvar! ' +
                                          'O erro foi reportado, tente novamente mais tarde.',
                                          reply_markup=ReplyKeyboardRemove())
                print(e)
                buff.pop(buff.index(item))
                return ConversationHandler.END

            buff.pop(buff.index(item))

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=item.stringData(),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=ReplyKeyboardRemove()
            )

            return ConversationHandler.END
        elif(update.message.text == 'Não, finalizar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!',
                reply_markup=ReplyKeyboardRemove())

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas com: ' +
                '"Sim, confirmar" ou "Não, finalizar"')

            update.message.reply_text(
                'Deseja confirmar o fechamento de intervalo?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return FIM_INTERVALO

    def saida(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'saida',
                                      datetime.now(timezone('America/Sao_Paulo')).replace(second=0, microsecond=0))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                if item.role == 'motorista':
                    motorista = session.query(Motorista).filter_by(
                        telegram_user=item.username).first()

                    pontoDb = session.query(PontosMotorista).filter_by(
                        motorista_id=motorista.id).order_by(PontosMotorista.entrada.desc()).first()
                else:
                    administrativo = session.query(Administrativo).filter_by(
                        telegram_user=item.username).first()
                    
                    pontoDb = session.query(PontosAdministrativo).filter_by(
                        administrativo_id=administrativo.id).order_by(PontosAdministrativo.entrada.desc()).first()

                pontoDb.entrada = item.entrada,
                pontoDb.saida = item.saida
                
                if item.role == 'motorista':
                    intervalos = session.query(IntervalosDePontoMotorista).filter_by(
                        ponto_motorista_id=pontoDb.id)
                    item.horas_extra = '00:00:00'
                else:
                    intervalos = session.query(IntervalosDePontoAdministrativo).filter_by(
                        ponto_administrativo_id=pontoDb.id)
                    item.horas_extra = '00:00:00'

                item.calculateHours(intervalos)

                pontoDb.horas_trabalhadas = item.horas_trabalhadas
                pontoDb.horas_extra = item.horas_extra 
                
                session.add(pontoDb)

                session.commit()

                if item.role == 'motorista':
                    intervalos = session.query(IntervalosDePontoMotorista).filter_by(
                        ponto_motorista_id=pontoDb.id)
                else:
                    intervalos = session.query(IntervalosDePontoAdministrativo).filter_by(
                        ponto_administrativo_id=pontoDb.id)
                
                item.intervalos = intervalos

                session.close()
            except Exception as e:
                update.message.reply_text('Houve um erro ao tentar salvar! ' +
                                          'O erro foi reportado, tente novamente mais tarde.',
                                          reply_markup=ReplyKeyboardRemove())
                print(e)
                buff.pop(buff.index(item))
                return ConversationHandler.END

            buff.pop(buff.index(item))

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=item.stringData(),
                parse_mode=ParseMode.MARKDOWN
            )

            return ConversationHandler.END
        elif(update.message.text == 'Não, finalizar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!',
                reply_markup=ReplyKeyboardRemove())

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas com: ' +
                '"Sim, confirmar" ou "Não, finalizar"',
                reply_markup=ReplyKeyboardRemove())

            update.message.reply_text(
                'Deseja confirmar o fechamento de expediente?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return SAIDA

    def reabertura(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'fim_intervalo',
                                      datetime.now(timezone('America/Sao_Paulo')).replace(second=0, microsecond=0))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                if item.role == 'motorista':
                    motorista = session.query(Motorista).filter_by(
                        telegram_user=item.username).first()

                    pontoDb = session.query(PontosMotorista).filter_by(
                        motorista_id=motorista.id).order_by(PontosMotorista.id.desc()).first()

                    intervalo = IntervalosDePontoMotorista(
                        pontoDb,
                        pontoDb.saida,
                        item.fim_intervalo
                    )
                else:
                    administrativo = session.query(Administrativo).filter_by(
                        telegram_user=item.username).first()
                    
                    pontoDb = session.query(PontosAdministrativo).filter_by(
                        administrativo_id=administrativo.id).order_by(PontosAdministrativo.id.desc()).first()
                    
                    intervalo = IntervalosDePontoAdministrativo(
                        pontoDb,
                        pontoDb.saida,
                        item.fim_intervalo
                    )

                pontoDb.saida = None

                session.add(intervalo)
                session.add(pontoDb)
                session.commit()

                if item.role == 'motorista':
                    intervalos = session.query(IntervalosDePontoMotorista).filter_by(
                        ponto_motorista_id=pontoDb.id)
                else:
                    intervalos = session.query(IntervalosDePontoAdministrativo).filter_by(
                        ponto_administrativo_id=pontoDb.id)
                
                item.intervalos = intervalos

                session.close()
            except Exception as e:
                update.message.reply_text('Houve um erro ao tentar salvar! ' +
                                          'O erro foi reportado, tente novamente mais tarde.',
                                          reply_markup=ReplyKeyboardRemove())
                print(e)
                buff.pop(buff.index(item))
                return ConversationHandler.END

            buff.pop(buff.index(item))
            item.saida = None

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=item.stringData(),
                parse_mode=ParseMode.MARKDOWN
            )

            return ConversationHandler.END
        elif(update.message.text == 'Não, finalizar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!',
                reply_markup=ReplyKeyboardRemove())

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas com: ' +
                '"Sim, confirmar" ou "Não, finalizar"')

            update.message.reply_text(
                'Deseja confirmar a reabertura de expediente?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return REABERTURA


    def cancel(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        buff.pop(buff.index(item))
        user = update.message.from_user
        self.logger.info("Usuario %s cancelou a conversa.", user.first_name)
        update.message.reply_text('Operação cancelada!',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
