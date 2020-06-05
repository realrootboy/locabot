from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from models.Motorista import Motorista
from models.PontosMotorista import PontosMotorista
from models.IntervalosDePontoMotorista import IntervalosDePontoMotorista
from models.regPonto import RegPonto
from models.Administrativo import Administrativo

from database.main import Database

class PontosMotorista:
    def __init__(self, logger):
        self.logger = logger
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('info_ponto', self.registro)],

            states={

            },

            fallbacks=[CommandHandler('cancelar_info_ponto', self.cancel)]
        )

    def registro(self, update, context):
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
