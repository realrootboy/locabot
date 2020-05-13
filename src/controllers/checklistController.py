from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from datetime import datetime

import shutil
import os

from controllers.controllerUtils import listUtils

from models.Checklist import Checklist
from models.Motorista import Motorista
from models.NaoConformidades import NaoConformidades

from models.regChecklist import RegChecklist

from database.main import Database

PLACA, KM_INICIAL, A_CONFIRM = range(3)

KM_FINAL = 0
CARRO_P_CASA = 1
VIAJOU_C_CARRO = 2
OUTRO_CONDUTOR = 3
NOVO_CONDUTOR = 4
DEIXOU_OFICINA = 5
LOCAL_OFICINA = 6
VAN_TACOGRAFO = 7
CALIBROU_PNEU = 8
MECANICA_MOTOR = 9
MECANICA_AMORTECEDOR = 10
MECANICA_ESCAPAMENTO = 11
MECANICA_FREIO = 12
MECANICA_EMBREAGEM = 13
MECANICA_ACELERADOR = 14
MECANICA_CAMBIO = 15
MECANICA_OLEO = 16
MECANICA_AGUA = 17
MECANICA_ALINHAMENTO = 18
MECANICA_FREIODEMAO = 19
MECANICA_CONFIRM = 20
F_CONFIRM = 21

buff = list()


class ChecklistController:
    def __init__(self, logger):
        self.logger = logger
        self.conv_handler_abertura = ConversationHandler(
            entry_points=[CommandHandler(
                'abrir_checklist', self.abrir_checklist)],

            states={
                PLACA: [MessageHandler(Filters.text, self.placa)],
                KM_INICIAL: [MessageHandler(Filters.text, self.km_inicial)],
                A_CONFIRM: [MessageHandler(Filters.text, self.a_confirm)]
            },

            fallbacks=[
                CommandHandler('Cancelar', self.cancel), 
                CommandHandler('cancelar', self.cancel)]
        )
        self.conv_handler_fechamento = ConversationHandler(
            entry_points=[CommandHandler(
                'fechar_checklist', self.fechar_checklist)],

            states={
                KM_FINAL: [MessageHandler(Filters.text, self.km_final)],
                
                CARRO_P_CASA: [MessageHandler(Filters.text, self.carro_p_casa)],
                VIAJOU_C_CARRO: [MessageHandler(Filters.text, self.viajou_c_carro)],
                OUTRO_CONDUTOR: [MessageHandler(Filters.text, self.outro_condutor)],
                NOVO_CONDUTOR: [MessageHandler(Filters.text, self.novo_condutor)],
                DEIXOU_OFICINA: [MessageHandler(Filters.text, self.deixou_oficina)],
                LOCAL_OFICINA: [MessageHandler(Filters.text, self.local_oficina)],
                VAN_TACOGRAFO: [MessageHandler(Filters.text, self.van_tacografo)],
                CALIBROU_PNEU: [MessageHandler(Filters.text, self.calibrou_pneu)],
                
                MECANICA_MOTOR: [MessageHandler(Filters.text, self.mecanica_motor)],
                MECANICA_AMORTECEDOR: [MessageHandler(Filters.text, self.mecanica_amortecedor)],
                MECANICA_ESCAPAMENTO: [MessageHandler(Filters.text, self.mecanica_escapamento)],
                MECANICA_FREIO: [MessageHandler(Filters.text, self.mecanica_freio)],
                MECANICA_EMBREAGEM: [MessageHandler(Filters.text, self.mecanica_embreagem)],
                MECANICA_ACELERADOR: [MessageHandler(Filters.text, self.mecanica_acelerador)],
                MECANICA_CAMBIO: [MessageHandler(Filters.text, self.mecanica_cambio)],
                MECANICA_OLEO: [MessageHandler(Filters.text, self.mecanica_oleo)],
                MECANICA_AGUA: [MessageHandler(Filters.text, self.mecanica_agua)],
                MECANICA_ALINHAMENTO: [MessageHandler(Filters.text, self.mecanica_alinhamento)],
                MECANICA_FREIODEMAO: [MessageHandler(Filters.text, self.mecanica_freiodemao)],
                MECANICA_CONFIRM: [MessageHandler(Filters.text, self.mecanica_confirm)],

                F_CONFIRM: [MessageHandler(Filters.text, self.f_confirm)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def abrir_checklist(self, update, context):
        try:
            open_checklist = RegChecklist(
                update.message.from_user.username, update.message.chat.id)
            buff.append(open_checklist)
        except:
            update.message.reply_text(
                'Não é possível realizar o cadastro de combustível sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        if update.message.from_user.username is None:
            update.message.reply_text(
                'Não é possível realizar o cadastro de combustível sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            buff.remove(open_checklist)
            return ConversationHandler.END

        try:
            Session = Database.Session
            session = Session()

            motorista = session.query(Motorista).filter_by(
                telegram_user=update.message.from_user.username).first()

            if motorista is None:
                update.message.reply_text(
                    'Usuário ' + update.message.from_user.username + ' não encontrado na base de dados. ' +
                    'Acesso não autorizado!', reply_markup=ReplyKeyboardRemove()
                )
                buff.remove(open_checklist)
                return ConversationHandler.END
            else:
                checklist = session.query(Checklist).filter_by(
                    motorista_id=motorista.id).order_by(Checklist.id.desc()).first()

            if checklist and not checklist.dt_fechamento:
                update.message.reply_text(
                    'Não foi possível abrir um novo checklist.\n\n*MOTIVO: existe um checklist em aberto*\n``` Por favor, feche-o antes de abrir um novo.```',
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode=ParseMode.MARKDOWN
                )
                buff.remove(open_checklist)
                return ConversationHandler.END

            session.close()
        except:
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        update.message.reply_text(
            'Olá, ' + motorista.nome + '. Por favor, informe a placa do veículo.', reply_markup=ReplyKeyboardRemove())

        return PLACA

    def placa(self, update, context):
        user = update.message.from_user

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'placa',
                                  update.message.text)

        self.logger.info("Placa informada por %s: %s",
                         user.first_name, update.message.text)
        update.message.reply_text(
            'Placa informada: '+update.message.text+'\n'
            'Agora informe a quilometragem inicial.')

        return KM_INICIAL

    def km_inicial(self, update, context):
        user = update.message.from_user

        try:
            if(float(update.message.text) < 0):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Quilometragem inválida. Por favor, informe novamente!')
                return KM_INICIAL
        except:
            replaced = str(update.message.text).replace(',', '.')
            try:
                if(float(replaced) < 0):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Quilometragem inválida. Por favor, informe novamente!')
                    return KM_INICIAL
            except:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Formato invalido de quilometragem. Por favor, informe novamente!')
                return KM_INICIAL

        replaced = str(update.message.text).replace('.', ',')

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'km_inicial',
                                  replaced)

        self.logger.info('Quilometragem informada por %s: %s',
                         user.first_name, update.message.text)
        update.message.reply_text(
            'Quilometragem informada: '+update.message.text+'\n')

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        update.message.reply_text(
            item.dadosAbertura(), parse_mode=ParseMode.MARKDOWN)

        reply_keyboard = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]

        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return A_CONFIRM

    def a_confirm(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...')

            try:
                Session = Database.Session
                session = Session()

                # motorista = Motorista('Renan Moreira Gomes', 'renanmgomes')
                motorista = session.query(Motorista).filter_by(
                    telegram_user=item.username).first()

                checklist = Checklist(
                    motorista,
                    item.placa,
                    str(item.km_inicial) + ' KM',
                    item.dt_abertura
                )

                session.add(checklist)
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

            return ConversationHandler.END
        elif(update.message.text == 'Não, refazer'):
            update.message.reply_text(
                'Ok! Vamos refazer então.',
                reply_markup=ReplyKeyboardMarkup([['Continuar']], one_time_keyboard=True))

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END

    def fechar_checklist(self, update, context):
        try:
            open_checklist = RegChecklist(
                update.message.from_user.username, update.message.chat.id)
        except:
            update.message.reply_text(
                'Não é possível realizar o cadastro de combustível sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        if update.message.from_user.username is None:
            update.message.reply_text(
                'Não é possível realizar o cadastro de combustível sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END

        try:
            Session = Database.Session
            session = Session()

            motorista = session.query(Motorista).filter_by(
                telegram_user=update.message.from_user.username).first()

            if motorista is None:
                update.message.reply_text(
                    'Usuário ' + update.message.from_user.username + ' não encontrado na base de dados. ' +
                    'Acesso não autorizado!', reply_markup=ReplyKeyboardRemove()
                )
                return ConversationHandler.END
            else:
                checklist = session.query(Checklist).filter_by(
                    motorista_id=motorista.id).order_by(Checklist.id.desc()).first()

            if checklist and not checklist.dt_fechamento:
                open_checklist.idd = checklist.id
                open_checklist.motorista_id = checklist.motorista_id
                open_checklist.placa = checklist.placa
                open_checklist.km_inicial = checklist.km_inicial

                buff.append(open_checklist)
            else:
                update.message.reply_text(
                    'Não foi possível abrir um novo checklist.\n\n*MOTIVO: existe um checklist em aberto*\n``` Por favor, feche-o antes de abrir um novo.```',
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode=ParseMode.MARKDOWN
                )
                return ConversationHandler.END

            session.close()
        except:
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        update.message.reply_text(
            'Olá, ' + motorista.nome + '. Por favor, informe a quilometragem final.', reply_markup=ReplyKeyboardRemove())

        return KM_FINAL

    def km_final(self, update, context):
        user = update.message.from_user
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        try:
            if(float(update.message.text) < 0):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Quilometragem inválida. Por favor, informe novamente!')
                update.message.reply_text(
                    'Por favor, informe novamente!',
                    reply_markup=ReplyKeyboardRemove())
                return KM_FINAL
            if(float(update.message.text) < float(item.km_inicial[:-3])):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Quilometragem final menor que a inicial (inicial:'+str(item.km_inicial)+').')
                update.message.reply_text(
                    'Por favor, informe novamente!',
                    reply_markup=ReplyKeyboardRemove())
                return KM_FINAL
        except:
            replaced = str(update.message.text).replace(',', '.')
            try:
                if(float(replaced) < 0):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Quilometragem inválida. Por favor, informe novamente!')
                    update.message.reply_text(
                        'Por favor, informe novamente!',
                        reply_markup=ReplyKeyboardRemove())
                    return KM_FINAL
                if(float(update.message.text) < float(item.km_inicial[:-3])):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Quilometragem final menor que a inicial (inicial:'+str(item.km_inicial)+').')
                    update.message.reply_text(
                        'Por favor, informe novamente!',
                        reply_markup=ReplyKeyboardRemove())
                    return KM_FINAL
            except:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Formato invalido de quilometragem.')
                update.message.reply_text(
                    'Por favor, informe novamente!',
                    reply_markup=ReplyKeyboardRemove())
                return KM_FINAL

        replaced = str(update.message.text).replace('.', ',')

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'km_final',
                                  replaced)

        self.logger.info('Quilometragem final informada por %s: %s',
                         user.first_name, update.message.text)
        update.message.reply_text(
            'Quilometragem final informada: '+update.message.text+'\n')

        reply_keyboard = [['Sim'], ['Não']]

        update.message.reply_text(
            'Retornou com o carro para casa?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CARRO_P_CASA

    def carro_p_casa(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        if(update.message.text == 'Sim'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'carro_p_casa',
                                      True)
        elif(update.message.text == 'Não'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'carro_p_casa',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Sim] ou [Não]')

            update.message.reply_text(
                'Retornou com o carro para casa?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return CARRO_P_CASA

        update.message.reply_text(
            'Viajou com o carro?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return VIAJOU_C_CARRO

    def viajou_c_carro(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        if(update.message.text == 'Sim'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'viajou_c_carro',
                                      True)
        elif(update.message.text == 'Não'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'viajou_c_carro',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Sim] ou [Não]')

            update.message.reply_text(
                'Outro condutor?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VIAJOU_C_CARRO

        update.message.reply_text(
            'Outro condutor?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return OUTRO_CONDUTOR

    def outro_condutor(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        if(update.message.text == 'Sim'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'outro_condutor',
                                      True)
            update.message.reply_text(
                'Insira o nome do novo condutor:',
                reply_markup=ReplyKeyboardRemove())

            return NOVO_CONDUTOR
        elif(update.message.text == 'Não'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'outro_condutor',
                                      False)
            update.message.reply_text(
                'Deixou na oficina?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return DEIXOU_OFICINA
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Sim] ou [Não]')

            update.message.reply_text(
                'Outro condutor?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return OUTRO_CONDUTOR

    def novo_condutor(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'novo_condutor',
                                  update.message.text)

        update.message.reply_text(
            'Deixou o carro na oficina (Revisão/Reforma)?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return DEIXOU_OFICINA

    def deixou_oficina(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        if(update.message.text == 'Sim'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'deixou_oficina',
                                      True)
            update.message.reply_text(
                'Informe a oficina(LOCAL):',
                reply_markup=ReplyKeyboardRemove())

            return LOCAL_OFICINA
        elif(update.message.text == 'Não'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'deixou_oficina',
                                      False)
            update.message.reply_text(
                'Trocou tacografo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return VAN_TACOGRAFO
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Sim] ou [Não]')

            update.message.reply_text(
                'Deixou o carro na oficina (Revisão/Reforma)?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return DEIXOU_OFICINA

    def local_oficina(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'local_oficina',
                                  update.message.text)

        update.message.reply_text(
            'Trocou tacografo?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return VAN_TACOGRAFO

    def van_tacografo(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        if(update.message.text == 'Sim'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'van_tacografo',
                                      True)
        elif(update.message.text == 'Não'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'van_tacografo',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Sim] ou [Não]')

            update.message.reply_text(
                'Trocou tacografo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VAN_TACOGRAFO

        update.message.reply_text(
            'Calibrou os Pneus?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CALIBROU_PNEU

    def calibrou_pneu(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Sim'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'calibrou_pneu',
                                      True)
        elif(update.message.text == 'Não'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'calibrou_pneu',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Sim] ou [Não]')

            update.message.reply_text(
                'Trocou tacografo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VAN_TACOGRAFO

        #reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
        #item = listUtils.searchAndGetItem(buff,
        #                                  update.message.from_user.username,
        #                                  update.message.chat.id)
        #update.message.reply_text(
        #    item.dadosFechamento(), parse_mode=ParseMode.MARKDOWN)
        #update.message.reply_text(
        #    'O dados informados estão corretos?',
        #    reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        #return F_CONFIRM

        context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a revisão da mecânica do veículo!')

        update.message.reply_text(
            'Como está o motor?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_MOTOR

    def mecanica_motor(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_motor',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_motor',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o motor?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_MOTOR
        
        update.message.reply_text(
            'Como está o amortecedor?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_AMORTECEDOR

    def mecanica_amortecedor(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_amortecedor',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_amortecedor',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o amortecedor?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_AMORTECEDOR
        
        update.message.reply_text(
            'Como está o escapamento?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_ESCAPAMENTO

    def mecanica_escapamento(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_escapamento',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_escapamento',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o escapamento?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_ESCAPAMENTO
        
        update.message.reply_text(
            'Como está o escapamento?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_FREIO

    def mecanica_freio(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_freio',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_freio',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o freio?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_FREIO
        
        update.message.reply_text(
            'Como está a embreagem?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_EMBREAGEM

    def mecanica_embreagem(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_embreagem',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_embreagem',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está a embreagem?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_EMBREAGEM
        
        update.message.reply_text(
            'Como está a embreagem?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_ACELERADOR

    def mecanica_acelerador(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_acelerador',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_acelerador',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o acelerador?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_ACELERADOR
        
        update.message.reply_text(
            'Como está o cambio?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_CAMBIO

    def mecanica_cambio(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_cambio',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_cambio',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o cambio?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_CAMBIO
        
        update.message.reply_text(
            'Como está o oleo?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_OLEO

    def mecanica_oleo(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_oleo',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_oleo',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o oleo?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_OLEO
        
        update.message.reply_text(
            'Como está a agua?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_AGUA

    def mecanica_agua(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_agua',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_agua',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está a agua?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_AGUA
        
        update.message.reply_text(
            'Como está o alinhamento?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_ALINHAMENTO

    def mecanica_alinhamento(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_alinhamento',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_alinhamento',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o alinhamento?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_ALINHAMENTO
        
        update.message.reply_text(
            'Como está o freio de mão?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MECANICA_FREIODEMAO

    def mecanica_freiodemao(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_freiodemao',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'mecanica_freiodemao',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                    'Como está o freio de mão?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_FREIODEMAO
        
        reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        update.message.reply_text(
            item.dadosMecanica(), parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        return MECANICA_CONFIRM

    def mecanica_confirm(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a revisão da lataria do veículo!')

            update.message.reply_text(
                'Como está o motor?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ConversationHandler.END
        elif(update.message.text == 'Não, refazer'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos novamente a revisão da mecanica do veículo!')
            
            update.message.reply_text(
            'Como está o motor?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_MOTOR
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END

    def f_confirm(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...')

            try:
                Session = Database.Session
                session = Session()

                checklist = session.query(Checklist).filter_by(
                    motorista_id=item.motorista_id).order_by(Checklist.id.desc()).first()

                checklist.km_final = item.km_final
                checklist.dt_fechamento = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")
                checklist.carro_p_casa = item.carro_p_casa
                checklist.viajou_c_carro = item.viajou_c_carro
                checklist.outro_condutor = item.outro_condutor
                checklist.novo_condutor = item.novo_condutor
                checklist.deixou_oficina = item.deixou_oficina
                checklist.local_oficina = item.local_oficina
                checklist.van_tacografo = item.van_tacografo
                checklist.calibrou_pneu = item.calibrou_pneu

                session.add(checklist)

                for i, nc in enumerate(item.desc_conformidades):
                    session.add(
                        NaoConformidades(
                            checklist,
                            item.media_dir + '/' + str(i) + '.jpg',
                            nc
                        )
                    )

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

            return ConversationHandler.END
        elif(update.message.text == 'Não, refazer'):
            update.message.reply_text(
                'Ok! Vamos refazer então.',
                reply_markup=ReplyKeyboardMarkup([['Continuar']], one_time_keyboard=True))

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END

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
