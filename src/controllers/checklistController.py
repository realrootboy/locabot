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
KM_FINAL, CONFORMIDADE, F_CONFORMIDADE, O_CONFORMIDADE = range(4)

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

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        self.conv_handler_fechamento = ConversationHandler(
            entry_points=[CommandHandler(
                'fechar_checklist', self.fechar_checklist)],

            states={
                KM_FINAL: [MessageHandler(Filters.text, self.km_final)],
                CONFORMIDADE: [MessageHandler(Filters.text, self.conformidade)],
                F_CONFORMIDADE: [MessageHandler(Filters.photo, self.f_conformidade)],
                O_CONFORMIDADE: [MessageHandler(Filters.text, self.o_conformidade)],
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

                #motorista = Motorista('Renan Moreira Gomes', 'renanmgomes')
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
                return KM_INICIAL
            if(float(update.message.text) < float(item.km_inicial[:-3])):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Quilometragem final menor que a inicial (inicial:'+str(item.km_inicial)+'). Por favor, informe novamente!')
                return KM_INICIAL
        except:
            replaced = str(update.message.text).replace(',', '.')
            try:
                if(float(replaced) < 0):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Quilometragem inválida. Por favor, informe novamente!')
                    return KM_INICIAL
                if(float(update.message.text) < float(item.km_inicial[:-3])):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Quilometragem final menor que a inicial (inicial:'+str(item.km_inicial)+'). Por favor, informe novamente!')
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
                                  'km_final',
                                  replaced)

        self.logger.info('Quilometragem final informada por %s: %s',
                         user.first_name, update.message.text)
        update.message.reply_text(
            'Quilometragem final informada: '+update.message.text+'\n')

        reply_keyboard = [['Sim, registrar'], ['Não, finalizar'], ['Cancelar']]

        update.message.reply_text(
            'Houve alguma não-conformidade?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CONFORMIDADE

    def conformidade(self, update, context):
        if(update.message.text == 'Sim, registrar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Por favor, envie a foto da não conformidade')
            return F_CONFORMIDADE
        elif(update.message.text == 'Não, finalizar'):
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)

            if(update.message.text == 'Não, finalizar'):
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

    def f_conformidade(self, update, context):
        try:
            file_id = update.message.photo[-1].file_id
            newFile = context.bot.getFile(file_id)
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            try:
                os.mkdir('media/'+item.media_dir)
            except Exception as e:
                print(e)

            newFile.download('media/' + item.media_dir + '/' +
                             str(item.n_conformidades) + '.jpg')

            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'n_conformidades',
                                      item.n_conformidades + 1)
        except Exception as e:
            print(e)
            update.message.reply_text(
                "Ocorreu um erro! Tente enviar apenas uma foto de uma vez. " +
                "Agora envie a foto da bomba antes do abastecimento."
            )
            listUtils.listItens(buff)
            return F_CONFORMIDADE

        update.message.reply_text(
            "Agora descreva a não-conformidade:"
        )

        return O_CONFORMIDADE

    def o_conformidade(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Salvando a não-conformidade...')

        item.desc_conformidades.append(update.message.text)
        aux = item.desc_conformidades

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'desc_conformidades',
                                  aux)
        
        print(aux)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Salvo com sucesso!'
        )

        reply_keyboard = [['Sim, registrar'], ['Não, finalizar'], ['Cancelar']]

        update.message.reply_text(
            'Houve mais alguma não-conformidade?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CONFORMIDADE

    def cancel(self, update, context):
        user = update.message.from_user
        self.logger.info("Usuario %s cancelou a conversa.", user.first_name)
        update.message.reply_text('Tchau!',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
