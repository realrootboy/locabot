from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from controllers.controllerUtils import listUtils

from models.Administrativo import Administrativo
from models.Checklist import Checklist
from models.IdentificacaoFalcao import IdentificacaoFalcao

from database.main import Database
from sqlalchemy.sql import func


class ChecklistExport:
    def __init__(self, logger):
        self.logger = logger
        self.info_checklist = CommandHandler('info_checklist', self.get_info)

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
            'da informação de checklist a ser consultada. \n\nEx: /info_checklist 5')
        else:
            try:
                arg_id = int(context.args[0])
            except:
                update.message.reply_text('O argumento repassado deve ser um número inteiro. \n\n' +
                'Ex: /info_checklist 20')
                session.close()
                return

            update.message.reply_text('Buscando registro...')
            checklist = session.query(Checklist).filter_by(id=arg_id).first()

            if Checklist is None:
                update.message.reply_text('Checklist não encontrado :(')
                session.close()
                return
            
            identificacao_falcao = session.query(IdentificacaoFalcao).filter_by(checklist_id=arg_id).first()

            reply = 'Cadastrado por: ' + checklist.motorista.nome + '\n'
            
            if(identificacao_falcao):
              reply += 'Identificado por: ' + identificacao_falcao.nome 
            
            update.message.reply_text(reply)

        session.close()

