from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from controllers.controllerUtils import listUtils

from models.Administrativo import Administrativo
from models.Registro import Registro

from database.main import Database
from sqlalchemy.sql import func


class CombustivelExport:
    def __init__(self, logger):
        self.logger = logger
        self.info_combustivel = CommandHandler('info_combustivel', self.get_info)

    def get_info(self, update, context):
        if update.message.from_user.username is None:
            update.message.reply_text(
                'Não é possível realizar a consulta sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return

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
                

        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return

        if len(context.args) < 1:
            update.message.reply_text('Ola, ' + administrativo.nome + ' por favor, informe o ID ' +
            'da informação de combustível a ser consultada. \n\nEx: /info_combustivel 5')
        else:
            try:
                arg_id = int(context.args[0])
            except:
                update.message.reply_text('O argumento repassado deve ser um número inteiro. \n\n' +
                'Ex: /info_combustivel 20')
                session.close()
                return

            update.message.reply_text('Buscando registro...')
            registro = session.query(Registro).filter_by(id=arg_id).first()

            if registro is None:
                update.message.reply_text('Registro não encontrado :(')
                session.close()
                return
            
            update.message.reply_text('Enviando as fotos...')

            context.bot.send_photo(update.effective_chat.id,caption='Bomba antes do abastecimento', photo=open('media/' + registro.media_dir + '/bomba_antes.jpg', 'rb'))
            context.bot.send_photo(update.effective_chat.id,caption='Bomba depois do abastecimento', photo=open('media/' + registro.media_dir + '/bomba_depois.jpg', 'rb'))
            context.bot.send_photo(update.effective_chat.id,caption='Nota fiscal', photo=open('media/' + registro.media_dir + '/nota_fiscal.jpg', 'rb'))
            context.bot.send_photo(update.effective_chat.id,caption='Painel do veículo', photo=open('media/' + registro.media_dir + '/painel.jpg', 'rb'))
            context.bot.send_photo(update.effective_chat.id,caption='Placa do veículo', photo=open('media/' + registro.media_dir + '/placa.jpg', 'rb'))

        session.close()

