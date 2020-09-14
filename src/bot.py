from controllers.pontoController import PontoController
from controllers.checklistController import ChecklistController
from controllers.combustivelController import CombustivelController

from views.ChecklistExport import ChecklistExport
from views.CombustivelExport import CombustivelExport
from views.PontosExport import PontosExport

from configs.bot import config
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode, 
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


class Locatransbot:
    def __init__(self):
        self.updater = Updater(config['token'], use_context=True)
        self.dp = self.updater.dispatcher

        self.loadControllers()
        self.loadViews()
        self.loadHandlers()

    def loadControllers(self):
        self.combustivel = CombustivelController(logger)
        self.checklist = ChecklistController(logger)
        self.ponto = PontoController(logger)
    
    def loadViews(self):
        self.checklist_views = ChecklistExport(logger)
        self.combustivel_views = CombustivelExport(logger)
        self.ponto_views = PontosExport(logger)

    def loadHandlers(self):
        self.dp.add_handler(self.combustivel.conv_handler)
        self.dp.add_handler(self.checklist.conv_handler_abertura)
        self.dp.add_handler(self.checklist.conv_handler_fechamento)
        self.dp.add_handler(self.ponto.conv_handler)
        self.dp.add_handler(self.ponto_views.conv_handler)
        self.dp.add_handler(self.ponto_views.disponiveis)
        self.dp.add_handler(self.ponto_views.falcao)
        self.dp.add_handler(self.combustivel_views.info_combustivel)
        self.dp.add_handler(self.checklist_views.info_checklist)

    def start(self):
        self.dp.add_handler(CommandHandler('start', self.startCommand))
        self.dp.add_error_handler(self.error)
        self.updater.start_polling()
        self.updater.idle()

    def startCommand(self, update, context):
        response_message = 'Interação com o bot ativada! Seja bem-vindo! =^._.^=\n\nAbrir Checklist\n/abrir_checklist\n\nFechar Checklist\n/fechar_checklist\n\nCadastrar Informações de Combustível\n/combustivel'

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=response_message
        )

    def error(self, update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)
