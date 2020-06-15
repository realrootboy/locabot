from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from models.Motorista import Motorista
from models.PontosMotorista import PontosMotorista
from models.IntervalosDePontoMotorista import IntervalosDePontoMotorista
from models.regPonto import RegPonto
from models.Administrativo import Administrativo
from models.PontosAdministrativo import PontosAdministrativo

from database.main import Database

ESCOLHA_ROLE = 1
ESCOLHA_ADMINISTRATIVO = 2
ESCOLHA_MOTORISTA = 3

class PontosMotorista:
    def __init__(self, logger):
        self.logger = logger
        self.conv_handler = ConversationHandler(
            entry_points=[CommandHandler('info_ponto', self.registro)],

            states={
                ESCOLHA_ROLE: [MessageHandler(Filters.text, self.escolha_role)],
                ESCOLHA_ADMINISTRATIVO: [MessageHandler(Filters.text, self.escolha_administrativo)],
                ESCOLHA_MOTORISTA: [MessageHandler(Filters.text, self.escolha_motorista)]
            },

            fallbacks=[CommandHandler('cancelar_info_ponto', self.cancel)]
        )

        self.disponiveis = CommandHandler('disponiveis', self.disponiveis)


    def disponiveis(self, update, context):
        disponiveis = '*DISPONIVEIS DO ADMINISTRATIVO*\n\n'

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
                return ConversationHandler.END

            adm_disponiveis = session.query(PontosAdministrativo).filter_by(
                saida=None)

            for item in adm_disponiveis:
                disponiveis += item.administrativo.nome + ' @' + item.administrativo.telegram_user +'\n'

        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        session.close()

        update.message.reply_text(disponiveis, reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)



    def registro(self, update, context):
        if update.message.from_user.username is None:
            update.message.reply_text(
                'Não é possível realizar a consulta de folha de ponto sem um nome de usuário cadastrado',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
        
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
                return ConversationHandler.END

        except Exception as e:
            print(e)
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        update.message.reply_text(
            'Olá, ' + administrativo.nome + '. Por favor, escolha o setor de consulta.',
            reply_markup=ReplyKeyboardMarkup([['Administrativo', 'Motorista']], one_time_keyboard=True))

        session.close()

        return ESCOLHA_ROLE
    
    def escolha_role(self, update, context):
        return

    def escolha_administrativo(self, update, context):
        return

    def escolha_motorista(self, update, context):
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
# import datetime
# import calendar
# 
# year = 2012
# month = 6
# 
# num_days = calendar.monthrange(year, month)[1]
# start_date = datetime.date(year, month, 1)
# end_date = datetime.date(year, month, num_days)
# 
# results = session.query(Event).filter(
#     and_(Event.date >= start_date, Event.date <= end_date)).all()
