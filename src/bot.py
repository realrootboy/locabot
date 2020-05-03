from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

from configs.bot import config
from controllers.combustivelController import CombustivelController
from controllers.checklistController import ChecklistController

class Locatransbot:
  def __init__(self):
    self.updater = Updater(config['token'], use_context=True)
    self.dp = self.updater.dispatcher
    
    self.combustivel = CombustivelController(logger)
    self.checklist = ChecklistController(logger)

    self.dp.add_handler(self.combustivel.conv_handler)
    self.dp.add_handler(self.checklist.conv_handler_abertura)
    self.dp.add_handler(self.checklist.conv_handler_fechamento)
    
  def start(self):
    self.dp.add_error_handler(self.error)
    self.updater.start_polling()
    self.updater.idle()

  def error(self, update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)