from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

import sys
sys.path.append('..')

from .controllerUtils import listUtils
from models.regAbastecimento import RegAbastecimento


RETORNO, PLACA, QUILOMETRAGEM, QNT_LITRO, VAL_LITRO, VAL_TOTAL, TP_COMBUSTIVEL, POSTO, CONFIRM = range(
    9)

buff = list()


class CombustivelController:
    def __init__(self, logger):
        self.logger = logger
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('combustivel', self.registro)],

            states={
                RETORNO: [MessageHandler(Filters.text, self.retorno)],
                PLACA: [MessageHandler(Filters.text, self.placa)],
                QUILOMETRAGEM: [MessageHandler(Filters.text, self.quilometragem)],
                QNT_LITRO: [MessageHandler(Filters.text, self.qnt_litro)],
                VAL_LITRO: [MessageHandler(Filters.text, self.val_litro)],
                TP_COMBUSTIVEL: [MessageHandler(Filters.text, self.tp_combustivel)],
                POSTO: [MessageHandler(Filters.text, self.posto)],
                CONFIRM: [MessageHandler(Filters.text, self.confirm)]
            },



            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def registro(self, update, context):
        update.message.reply_text(
            'Olá, motorista! Por favor, informe a placa do veículo.', reply_markup=ReplyKeyboardRemove())
        abastecimento = RegAbastecimento(
            update.message.from_user.username, update.message.chat.id)
        buff.append(abastecimento)

        return PLACA

    def retorno(self, update, context):
        update.message.reply_text(
            'Olá, motorista! Por favor, informe a placa do veículo.', reply_markup=ReplyKeyboardRemove())

        abastecimento = RegAbastecimento(
            update.message.from_user.username, update.message.chat.id)

        buff.append(abastecimento)
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
            'Agora nos informe a quilometragem atual.')

        return QUILOMETRAGEM

    def quilometragem(self, update, context):
        user = update.message.from_user

        try:
            if(float(update.message.text) < 0):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Quilometragem inválida. Por favor, informe novamente!')
                return QUILOMETRAGEM
        except:
            replaced = str(update.message.text).replace(',', '.')
            try:
                if(float(replaced) < 0):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Quilometragem inválida. Por favor, informe novamente!')
                    return QUILOMETRAGEM
            except:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Formato invalido de quilometragem. Por favor, informe novamente!')
                return QUILOMETRAGEM

        replaced = str(update.message.text).replace('.', ',')

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'quilometragem',
                                  replaced)

        self.logger.info('Quilometragem informada por %s: %s',
                         user.first_name, update.message.text)
        update.message.reply_text(
            'Quilometragem informada: '+update.message.text+'\n'
            'Agora nos informe a quantidade de litros abastecidos')

        return QNT_LITRO

    def qnt_litro(self, update, context):
        user = update.message.from_user

        try:
            if(float(update.message.text) < 0):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Quantidade de litros inválidos. Por favor, informe novamente!')
                return QNT_LITRO
        except:
            replaced = str(update.message.text).replace(',', '.')
            try:
                if(float(replaced) < 0):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Quantidade de litros inválidos. Por favor, informe novamente!')
                    return QNT_LITRO
            except:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Formato invalido de quantidade de litros. Por favor, informe novamente!')
                return QNT_LITRO

        replaced = str(update.message.text).replace('.', ',')

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'qnt_litro',
                                  replaced)

        self.logger.info('Quantidade de litros informada por %s: %s',
                         user.first_name, update.message.text)
        update.message.reply_text(
            'Quantidade de litros informados: '+update.message.text+'\n'
            'Agora informe o valor do litro:')

        return VAL_LITRO

    def val_litro(self, update, context):
        user = update.message.from_user

        try:
            if(float(update.message.text) < 0):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Valor do litro inválido. Por favor, informe novamente!')
                return VAL_LITRO
        except:
            replaced = str(update.message.text).replace(',', '.')
            try:
                if(float(replaced) < 0):
                    context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Valor do litro inválido. Por favor, informe novamente!')
                    return VAL_LITRO
            except:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Formato invalido de valor do litro. Por favor, informe novamente!')
                return VAL_LITRO

        replaced = str(update.message.text).replace('.', ',')

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'val_litro',
                                  replaced)

        self.logger.info('Valor do litro informado por %s: %s',
                         user.first_name, update.message.text)

        # update.message.reply_text(
        #     'Valor do litro informado: '+update.message.text+'\n'
        #     'Agora informe o valor total:')

        reply_keyboard = [['DIESEL COMUM', 'DIESEL S-10'],
                          ['GASOLINA ADITIVIDADA', 'GASOLINA COMUM']]

        update.message.reply_text(
            'Valor do litro informado: '+update.message.text+'\n'
            'Agora informe o tipo de combustivel:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        # return VAL_TOTAL
        return TP_COMBUSTIVEL

    def tp_combustivel(self, update, context):
        user = update.message.from_user

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'tp_combustivel',
                                  update.message.text)

        self.logger.info('Combustivel informado por %s: %s',
                         user.first_name, update.message.text)

        reply_keyboard = [['MARLIN', 'LIDER'],
                          ['OURO NEGRO', 'RIO NEGRO'],
                          ['DAMIANI', 'JR / DALLAS'],
                          ['TIMBOZAO / TREMENDAO', 'RAIZ']]

        update.message.reply_text(
            'Combustível informado: '+update.message.text+'\n'
            'Agora informe o posto:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return POSTO

    def posto(self, update, context):
        user = update.message.from_user

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'posto',
                                  update.message.text)

        self.logger.info('Posto informado por %s: %s',
                         user.first_name, update.message.text)

        item = listUtils.searchAndGetItem(buff,
                                update.message.from_user.username,
                                update.message.chat.id)

        a = float(str(item.qnt_litro).replace(',', '.'))
        b = float(str(item.val_litro).replace(',', '.'))
        item.val_total = str(float(a*b)).replace('.', ',')

        update.message.reply_text(
            item.stringData(), parse_mode=ParseMode.MARKDOWN)

        reply_keyboard = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]

        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CONFIRM

    def confirm(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                update.message.from_user.username,
                                update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...')

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            return ConversationHandler.END
        elif(update.message.text == 'Não, refazer'):
            update.message.reply_text(
                'Ok! Vamos refazer então.',
                reply_markup=ReplyKeyboardMarkup([['Continuar']], one_time_keyboard=True))
            buff.pop(buff.index(item))
            return RETORNO
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')
            return ConversationHandler.END

    def cancel(self, update, context):
        user = update.message.from_user
        self.logger.info("Usuario %s cancelou a conversa.", user.first_name)
        update.message.reply_text('Tchau!',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END
