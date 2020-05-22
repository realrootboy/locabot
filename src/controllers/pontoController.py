from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from datetime import datetime
from pytz import timezone

from controllers.controllerUtils import listUtils

from models.Motorista import Motorista
from models.PontosMotorista import PontosMotorista

from models.regPonto import RegPonto

from database.main import Database

OPTS, ENTRADA, INTERVALO, FIM_INTERVALO, SAIDA = range(5)
buff = list()


def handleOpts(ponto):
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
                OPTS: [MessageHandler(Filters.text, self.opts)],
                ENTRADA: [MessageHandler(Filters.text, self.entrada)],
                INTERVALO: [MessageHandler(Filters.text, self.intervalo)],
                FIM_INTERVALO: [MessageHandler(Filters.text, self.fim_intervalo)],
                SAIDA: [MessageHandler(Filters.text, self.saida)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def registro(self, update, context):
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

        try:
            Session = Database.Session
            session = Session()

            motorista = session.query(Motorista).filter_by(
                telegram_user=ponto.username
            ).first()

            if motorista is None:
                session.close()
                return ConversationHandler.END
            else:
                pontoDb = session.query(PontosMotorista).filter_by(
                    motorista_id=motorista.id).order_by(PontosMotorista.id.desc()).first()
                ponto.role = 'motorista'
                nome = motorista.nome

                if(pontoDb and pontoDb.saida is None):
                    ponto.entrada = pontoDb.entrada
                    ponto.intervalo = pontoDb.intervalo
                    ponto.fim_intervalo = pontoDb.fim_intervalo
                    ponto.saida = pontoDb.saida
        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

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
                                  datetime.now(timezone('America/Sao_Paulo')))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                motorista = session.query(Motorista).filter_by(
                    telegram_user=item.username).first()
                
                ponto = PontosMotorista(
                    motorista,
                    item.entrada,
                    item.intervalo,
                    item.fim_intervalo,
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
                text='Operação cancelada!')

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
                                  datetime.now(timezone('America/Sao_Paulo')))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                motorista = session.query(Motorista).filter_by(
                    telegram_user=item.username).first()
                
                pontoDb = session.query(PontosMotorista).filter_by(
                    motorista_id=motorista.id).order_by(PontosMotorista.id.desc()).first()
                
                pontoDb.entrada = item.entrada,
                pontoDb.intervalo = item.intervalo,
                pontoDb.fim_intervalo = item.fim_intervalo,
                pontoDb.saida = item.saida                    
                
                session.add(pontoDb)

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
                text='Operação cancelada!')

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
                                  datetime.now(timezone('America/Sao_Paulo')))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                motorista = session.query(Motorista).filter_by(
                    telegram_user=item.username).first()
                
                pontoDb = session.query(PontosMotorista).filter_by(
                    motorista_id=motorista.id).order_by(PontosMotorista.id.desc()).first()
                
                pontoDb.entrada = item.entrada,
                pontoDb.intervalo = item.intervalo,
                pontoDb.fim_intervalo = item.fim_intervalo,
                pontoDb.saida = item.saida                    
                
                session.add(pontoDb)

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
                text='Operação cancelada!')

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
                                  datetime.now(timezone('America/Sao_Paulo')))

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...'
            )

            try:
                Session = Database.Session
                session = Session()

                motorista = session.query(Motorista).filter_by(
                    telegram_user=item.username).first()
                
                pontoDb = session.query(PontosMotorista).filter_by(
                    motorista_id=motorista.id).order_by(PontosMotorista.id.desc()).first()
                
                pontoDb.entrada = item.entrada,
                pontoDb.intervalo = item.intervalo,
                pontoDb.fim_intervalo = item.fim_intervalo,
                pontoDb.saida = item.saida                    
                
                session.add(pontoDb)

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
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas com: ' +
                '"Sim, confirmar" ou "Não, finalizar"')
            
            update.message.reply_text(
                'Deseja confirmar o fechamento de expediente?',
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, finalizar']], one_time_keyboard=True)
            )

            return SAIDA

    def cancel(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        buff.pop(buff.index(item))
        user = update.message.from_user
        self.logger.info("Usuario %s cancelou a conversa.", user.first_name)
        update.message.reply_text('Tchau!',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
