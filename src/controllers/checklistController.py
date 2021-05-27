from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode,
                      InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

from datetime import datetime
from pytz import timezone

import xlsxwriter
import shutil
import os

from controllers.controllerUtils import listUtils

from models.Checklist import Checklist
from models.Motorista import Motorista
from models.NaoConformidades import NaoConformidades
from models.IdentificacaoFalcao import IdentificacaoFalcao
from models.Veiculos import Veiculos

from models.regChecklist import RegChecklist

from utils import textLogger
from utils import CalendarUtils
from drive import gdrive

from database.main import Database

PLACA = -3
KM_INICIAL = -2
A_CONFIRM = 71

KM_FINAL = 0

CARRO_P_CASA = 1
VIAJOU_C_CARRO = 2
OUTRO_CONDUTOR = 3
NOVO_CONDUTOR = 4
DEIXOU_OFICINA = 5
LOCAL_OFICINA = 6
VAN_TACOGRAFO = 7
CALIBROU_PNEU = 8

MENU_DINAMICO = 9

F_CONFIRM = 70

CONFORMIDADE = 72
F_CONFORMIDADE = 73
O_CONFORMIDADE = 74

MENU_SWITCHER = 75

KM_CONFIRM = 76

MANUAL = 77
CHAVE_RESERVA = 78

MOTIVO = 79

NOME_FALCAO = 80

CRLV = 81

buff = list()

ASSOC = {
    'mecanica': [('mecanica', 'Mecânica'),
                 ('motor', 'Motor'),
                 ('amortecedor', 'Amortecedor'),
                 ('escapamento', 'Escapamento'),
                 ('freio', 'Freio'),
                 ('embreagem', 'Embreagem'),
                 ('acelerador', 'Acelerador'),
                 ('cambio', 'Câmbio'),
                 ('oleo', 'Òleo'),
                 ('agua', 'Agua'),
                 ('alinhamento', 'Alinhamento'),
                 ('freiodemao', 'Freio de mão')],
    'lataria': [('lataria', 'Lataria'),
                ('dianteiro', 'Lataria dianteira'),
                ('traseiro', 'Lateria traseira'),
                ('portadianteiradireita', 'Porta dianteira direita'),
                ('portadianteiraesquerda', 'Porta dianteira esquerda'),
                ('portatraseiradireita', 'Porta traseira direita'),
                ('portatraseiraesquerda', 'Porta traseira esquerda'),
                ('portamalas', 'Porta-malas'),
                ('parachoquedianteiro', 'Parachoque dianteiro'),
                ('parachoquetraseiro', 'Parachoque traseiro')],
    'eletrica': [('eletrica', 'Elétrica'),
                 ('farolete', 'Farolete'),
                 ('farolbaixo', 'Farol baixo'),
                 ('farolalto', 'Farol alto'),
                 ('setas', 'Setas'),
                 ('luzesdopainel', 'Luzes do painel'),
                 ('luzesinternas', 'Luzes internas'),
                 ('bateria', 'Bateria'),
                 ('radio', 'Radio'),
                 ('altofalantes', 'Alto falantes'),
                 ('limpadorparabrisa', 'Limpador de parabrisa'),
                 ('arcondicionado', 'Ar condicionado'),
                 ('travas', 'Travas'),
                 ('vidros', 'Vidros')],
    'vidros': [('vidros', 'Vidros'),
               ('parabrisa', 'Parabrisa'),
               ('lateraisesquerdo', 'Laterais esquerdo'),
               ('lateraisdireito', 'Laterais direito'),
               ('traseiro', 'Traseiro')],
    'seguranca': [('seguranca', 'Segurança'),
                  ('triangulo', 'Triangulo'),
                  ('extintor', 'Extintor'),
                  ('cintos', 'Cintos'),
                  ('alarme', 'Alarme'),
                  ('fechaduras', 'Fechaduras'),
                  ('macanetas', 'Maçanetas'),
                  ('retrovisores', 'Retrovisores'),
                  ('macaco', 'Macaco')],
    'pneus': [('pneus', 'Pneus'),
              ('dianteiroesquerdo', 'Dianteiro esquerdo'),
              ('dianteirodireito', 'Dianteiro direito'),
              ('traseiroesquerdo', 'Traseiro esquerdo'),
              ('traseiroedireito', 'Traseiro direito'),
              ('estepe', 'Estepe')],
    'higienizacao': [('higienizacao', 'Higienização'),
                     ('externa', 'Higienização externa'),
                     ('interna', 'Higienização interna')]
}

valid_in_switcher = list(map(str, list(range(1, len(ASSOC) + 3))))

menu_itens = ''
for index, key in enumerate(ASSOC):
    menu_itens += str(index + 1) + ' - ' + ASSOC[key][0][1] + '\n'

str_menu = 'Por favor, escolha o grupo de itens desejado para iniciar a revisao:\n\n' + \
    menu_itens + '8 - CONTINUAR OPERAÇÃO\n9 - CANCELAR OPERAÇÃO'


def keyboardMenu(opts=0):
    keyboard = []

    if opts == 0:
        return keyboard

    append_count = 0
    arr = list(map(str, list(range(1, opts + 1))))
    for index, a in enumerate(zip(arr, arr[1:], arr[2:])):
        if index % 3 == 0:
            keyboard.append(list(a))
            append_count = append_count + 1

    keyboard.append(arr[3*append_count:])
    return keyboard


def dynamic_menu(group):
    group_send = ASSOC[group][0][1]
    str_menu = 'Por favor, selecione o item de ' + \
        group_send + ' que *NÃO ESTÁ OK*\n\n'
    for index, a in enumerate(ASSOC[group][1:]):
        str_menu += str(index + 1) + ' - ' + a[1] + '\n'
    str_menu += str(len(ASSOC[group][1:]) + 1) + ' - VOLTAR'
    return str_menu


class ChecklistController:
    def __init__(self, logger):
        self.logger = logger
        self.conv_handler_abertura = ConversationHandler(
            entry_points=[CommandHandler(
                'abrir_checklist', self.abrir_checklist)],

            states={
                PLACA: [MessageHandler(Filters.text & (~ Filters.command), self.placa)],
                KM_INICIAL: [MessageHandler(Filters.text & (~ Filters.command), self.km_inicial)],
                A_CONFIRM: [MessageHandler(Filters.text & (~ Filters.command), self.a_confirm)],

                MOTIVO: [MessageHandler(Filters.text & (~ Filters.command), self.motivo)],

                NOME_FALCAO: [MessageHandler(Filters.text & (~ Filters.command), self.nome_falcao)],

                MANUAL: [MessageHandler(Filters.text & (~ Filters.command), self.manual)],
                CRLV: [MessageHandler(Filters.text & (~ Filters.command), self.crlv)],

                CARRO_P_CASA: [MessageHandler(Filters.text & (~ Filters.command), self.carro_p_casa)],
                VIAJOU_C_CARRO: [MessageHandler(Filters.text & (~ Filters.command), self.viajou_c_carro)],
                OUTRO_CONDUTOR: [MessageHandler(Filters.text & (~ Filters.command), self.outro_condutor)],
                NOVO_CONDUTOR: [MessageHandler(Filters.text & (~ Filters.command), self.novo_condutor)],
                DEIXOU_OFICINA: [MessageHandler(Filters.text & (~ Filters.command), self.deixou_oficina)],
                LOCAL_OFICINA: [MessageHandler(Filters.text & (~ Filters.command), self.local_oficina)],
                VAN_TACOGRAFO: [MessageHandler(Filters.text & (~ Filters.command), self.van_tacografo)],
                CALIBROU_PNEU: [MessageHandler(Filters.text & (~ Filters.command), self.calibrou_pneu)],

                MENU_DINAMICO: [MessageHandler(Filters.text & (~ Filters.command), self.menu_dinamico)],

                MENU_SWITCHER: [MessageHandler(Filters.text & (~ Filters.command), self.menu_switcher)],
                KM_CONFIRM: [MessageHandler(Filters.text & (~ Filters.command), self.km_confirm)],

                CONFORMIDADE: [MessageHandler(Filters.text & (~ Filters.command), self.conformidade)],
                F_CONFORMIDADE: [MessageHandler(Filters.photo, self.f_conformidade)],
                O_CONFORMIDADE: [MessageHandler(
                    Filters.text & (~ Filters.command), self.o_conformidade)]

            },

            fallbacks=[
                CommandHandler('cancelar', self.cancel)]
        )
        self.conv_handler_fechamento = ConversationHandler(
            entry_points=[CommandHandler(
                'fechar_checklist', self.fechar_checklist)],

            states={
                KM_FINAL: [MessageHandler(Filters.text & (~ Filters.command), self.km_final)],

                CARRO_P_CASA: [MessageHandler(Filters.text & (~ Filters.command), self.carro_p_casa)],
                VIAJOU_C_CARRO: [MessageHandler(Filters.text & (~ Filters.command), self.viajou_c_carro)],
                OUTRO_CONDUTOR: [MessageHandler(Filters.text & (~ Filters.command), self.outro_condutor)],
                NOVO_CONDUTOR: [MessageHandler(Filters.text & (~ Filters.command), self.novo_condutor)],
                DEIXOU_OFICINA: [MessageHandler(Filters.text & (~ Filters.command), self.deixou_oficina)],
                LOCAL_OFICINA: [MessageHandler(Filters.text & (~ Filters.command), self.local_oficina)],
                VAN_TACOGRAFO: [MessageHandler(Filters.text & (~ Filters.command), self.van_tacografo)],
                CALIBROU_PNEU: [MessageHandler(Filters.text & (~ Filters.command), self.calibrou_pneu)],

                MENU_DINAMICO: [MessageHandler(Filters.text & (~ Filters.command), self.menu_dinamico)],

                MOTIVO: [MessageHandler(Filters.text & (~ Filters.command), self.motivo)],

                MANUAL: [MessageHandler(Filters.text & (~ Filters.command), self.manual)],
                CRLV: [MessageHandler(Filters.text & (~ Filters.command), self.crlv)],

                MENU_SWITCHER: [MessageHandler(Filters.text & (~ Filters.command), self.menu_switcher)],
                KM_CONFIRM: [MessageHandler(Filters.text & (~ Filters.command), self.km_confirm)],

                F_CONFIRM: [MessageHandler(Filters.text & (~ Filters.command), self.f_confirm)],

                CONFORMIDADE: [MessageHandler(Filters.text & (~ Filters.command), self.conformidade)],
                F_CONFORMIDADE: [MessageHandler(Filters.photo, self.f_conformidade)],
                O_CONFORMIDADE: [MessageHandler(
                    Filters.text & (~ Filters.command), self.o_conformidade)]
            },

            fallbacks=[CommandHandler('cancelar', self.cancel)]
        )

    def abrir_checklist(self, update, context):
        placas = [['CANCELAR']]

        if update.callback_query:
            try:
                current_chat_id = update.callback_query.message.chat.id
                current_username = update.callback_query.from_user.username
                open_checklist = RegChecklist(
                    current_username, current_chat_id, True)
                buff.append(open_checklist)
            except Exception as e:
                context.bot.send_message(
                    chat_id=current_chat_id,
                    text='Não é possível realizar o cadastro de checklist sem um nome de usuário cadastrado.')
                return ConversationHandler.END
        else:
            try:
                current_chat_id = update.message.chat.id
                current_username = update.message.from_user.username
                open_checklist = RegChecklist(
                    current_username, current_chat_id, True)
                buff.append(open_checklist)
            except Exception as e:
                print(e)
                update.message.reply_text(
                    'Não é possível realizar o cadastro de checklist sem um nome de usuário cadastrado.',
                    reply_markup=ReplyKeyboardRemove()
                )
                return ConversationHandler.END

        try:
            Session = Database.Session
            session = Session()

            motorista = session.query(Motorista).filter_by(
                telegram_user=current_username).first()

            if motorista is None:
                context.bot.send_message(
                    chat_id=current_chat_id,
                    text='Usuário ' + current_username + ' não encontrado na base de dados. ' +
                    'Acesso não autorizado!', reply_markup=ReplyKeyboardRemove()
                )
                buff.remove(open_checklist)
                session.close()
                return ConversationHandler.END
            else:
                checklist = session.query(Checklist).filter_by(
                    motorista_id=motorista.id).order_by(Checklist.id.desc()).first()

            if checklist and not checklist.dt_fechamento:
                context.bot.send_message(
                    chat_id=current_chat_id,
                    text='Não foi possível abrir um novo checklist.\n\n*MOTIVO: existe um checklist em aberto*\n``` Por favor, feche-o antes de abrir um novo.```',
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode=ParseMode.MARKDOWN
                )
                buff.remove(open_checklist)
                session.close()
                return ConversationHandler.END

            veiculos = session.query(Veiculos).order_by(Veiculos.placa.asc())

            for veiculo in veiculos:
                placas.append([veiculo.placa])

            session.close()
        except Exception as e:
            print(e)
            context.bot.send_message(
                chat_id=current_chat_id,
                text='Houve um erro ao tentar se conectar com a base de dados! ' +
                     'O erro foi reportado, tente novamente mais tarde.',
                     reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        context.bot.send_message(
            chat_id=current_chat_id,
            text='Olá, ' + motorista.nome +
            '. Por favor, informe a placa do veículo ou digite "CANCELAR" para cancelar a operação',
            reply_markup=ReplyKeyboardMarkup(placas, one_time_keyboard=True))

        return PLACA

    def placa(self, update, context):

        if(str(update.message.text).upper() == 'CANCELAR'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            buff.pop(buff.index(item))

            return ConversationHandler.END

        user = update.message.from_user

        Session = Database.Session
        session = Session()

        placa = session.query(Veiculos).filter_by(
            placa=update.message.text).first()

        if placa is None:
            placas = [['CANCELAR']]
            veiculos = session.query(Veiculos).order_by(Veiculos.placa.asc())

            for veiculo in veiculos:
                placas.append([veiculo.placa])

            update.message.reply_text(
                'Placa ' + update.message.text + ' inválida ou não encontrada na base de dados. ' +
                'Por favor, informe novamente a placa do veículo ou digite "CANCELAR" para cancelar a operação',
                reply_markup=ReplyKeyboardMarkup(placas, one_time_keyboard=True))
            session.close()
            return PLACA

        session.close()

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

        reply_keyboard = [['Sim'], ['Não']]

        update.message.reply_text(
            'Quilometragem enviada: ' + update.message.text + ' KM\n\n' +
            'A quilometragem foi inserida corretamente?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return KM_CONFIRM

    def km_confirm(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if item.is_abertura:
            informado = item.km_inicial
            question_header = 'Por favor, informe o motivo de abertura de checklist:'
            reply_keyboard2 = [['OS'], ['Manutenção'], ['Outro']]
        else:
            informado = item.km_final
            question_header = 'Por favor, informe o motivo de fechamento de checklist:'
            reply_keyboard2 = [['Finalização de Serviço'],
                               ['Manutenção'], ['Outro']]

        if(str(update.message.text).upper() == 'SIM'):
            update.message.reply_text(
                question_header,
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

            return MOTIVO
        elif(str(update.message.text).upper() == 'NÃO'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Por favor, informe novamente!')
            if item.is_abertura:
                return KM_INICIAL
            else:
                return KM_FINAL
        else:
            update.message.reply_text(
                'Opção inválida! Por favor, responda apenas: "Sim" ou "Não"'
            )

            update.message.reply_text(
                'Quilometragem enviada: ' + informado + ' KM\n\n' +
                'A quilometragem foi inserida corretamente?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return KM_CONFIRM

    def motivo(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'motivo',
                                  update.message.text)

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        update.message.reply_text(
            'O manual está no veículo?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MANUAL

    def nome_falcao(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'nome_falcao',
                                  update.message.text)

        update.message.reply_text(
            'O manual está no veículo?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return MANUAL

    def manual(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(str(update.message.text).upper() == 'SIM'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'manual',
                                      True)
            update.message.reply_text(
                'O documento do veículo (CRLV) está no veículo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            
            return CRLV
        elif(str(update.message.text).upper() == 'NÃO'):
            print(update.message.text)
            try:
                listUtils.searchAndUpdate(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id,
                                          'manual',
                                          False)
            except Exception as e:
                print(e)
            update.message.reply_text(
                'O documento do veículo (CRLV) está no veículo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            
            return CRLV
        else:
            update.message.reply_text(
                'Opção inválida! Por favor, responda apenas: "Sim" ou "Não"'
            )

            update.message.reply_text(
                'O manual está no veículo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MANUAL
    
    def crlv(self, update, context):
        reply_keyboard = [['Sim'], ['Não']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(str(update.message.text).upper() == 'SIM'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'crlv',
                                      True)
            if(item.is_abertura):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=str_menu,
                    reply_markup=ReplyKeyboardMarkup(keyboardMenu(9))
                )
                return MENU_SWITCHER
            else:
                update.message.reply_text(
                    'Retornou com o carro para casa?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                return CARRO_P_CASA
        elif(str(update.message.text).upper() == 'NÃO'):
            print(update.message.text)
            try:
                listUtils.searchAndUpdate(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id,
                                          'crlv',
                                          False)
            except Exception as e:
                print(e)
            if(item.is_abertura):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=str_menu,
                    reply_markup=ReplyKeyboardMarkup(keyboardMenu(9))
                )
                return MENU_SWITCHER
            else:
                update.message.reply_text(
                    'Retornou com o carro para casa?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
                return CARRO_P_CASA
        else:
            update.message.reply_text(
                'Opção inválida! Por favor, responda apenas: "Sim" ou "Não"'
            )

            update.message.reply_text(
                'O documento do veículo (CRLV) está no veículo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return CRLV

    # def chave_reserva(self, update, context):
    #    reply_keyboard = [['Sim'], ['Não']]
    #    item = listUtils.searchAndGetItem(buff,
    #                                      update.message.from_user.username,
    #                                      update.message.chat.id)
    #
    #    if(str(update.message.text).upper() == 'SIM'):
    #        listUtils.searchAndUpdate(buff,
    #                                  update.message.from_user.username,
    #                                  update.message.chat.id,
    #                                  'chave_reserva',
    #                                  True)
    #        if(item.is_abertura):
    #            context.bot.send_message(
    #                chat_id=update.effective_chat.id,
    #                text=str_menu,
    #                reply_markup=ReplyKeyboardMarkup(keyboardMenu(9))
    #            )
    #            return MENU_SWITCHER
    #        else:
    #            update.message.reply_text(
    #                'Retornou com o carro para casa?',
    #                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    #            return CARRO_P_CASA
    #    elif(str(update.message.text).upper() == 'NÃO'):
    #        listUtils.searchAndUpdate(buff,
    #                                  update.message.from_user.username,
    #                                  update.message.chat.id,
    #                                  'chave_reserva',
    #                                  False)
    #        if(item.is_abertura):
    #            context.bot.send_message(
    #                chat_id=update.effective_chat.id,
    #                    text=str_menu,
    #                    reply_markup=ReplyKeyboardMarkup(keyboardMenu(9))
    #                )
    #            return MENU_SWITCHER
    #        else:
    #            update.message.reply_text(
    #                'Retornou com o carro para casa?',
    #                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    #            return CARRO_P_CASA
    #    else:
    #        update.message.reply_text(
    #            'Opção inválida! Por favor, responda apenas: "Sim" ou "Não"'
    #        )
    #        update.message.reply_text(
    #            'A chave reserva está no veículo?',
    #            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    #
    #        return CHAVE_RESERVA

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
                    True,
                    item.placa,
                    str(item.km_inicial) + ' KM',
                    datetime.now(timezone('America/Sao_Paulo'))
                )

                checklist.carro_p_casa = item.carro_p_casa
                checklist.viajou_c_carro = item.viajou_c_carro
                checklist.manual = item.manual
                checklist.crlv = item.crlv
                checklist.motivo = item.motivo
                checklist.chave_reserva = item.chave_reserva
                checklist.outro_condutor = item.outro_condutor
                checklist.novo_condutor = item.novo_condutor
                checklist.deixou_oficina = item.deixou_oficina
                checklist.local_oficina = item.local_oficina
                checklist.van_tacografo = item.van_tacografo
                checklist.calibrou_pneu = item.calibrou_pneu
                checklist.mecanica_motor = item.mecanica_motor
                checklist.mecanica_amortecedor = item.mecanica_amortecedor
                checklist.mecanica_escapamento = item.mecanica_escapamento
                checklist.mecanica_freio = item.mecanica_freio
                checklist.mecanica_embreagem = item.mecanica_embreagem
                checklist.mecanica_acelerador = item.mecanica_acelerador
                checklist.mecanica_cambio = item.mecanica_cambio
                checklist.mecanica_oleo = item.mecanica_oleo
                checklist.mecanica_agua = item.mecanica_agua
                checklist.mecanica_alinhamento = item.mecanica_alinhamento
                checklist.mecanica_freiodemao = item.mecanica_freiodemao
                checklist.lataria_dianteiro = item.lataria_dianteiro
                checklist.lataria_traseiro = item.lataria_traseiro
                checklist.lataria_portadianteiradireita = item.lataria_portadianteiradireita
                checklist.lataria_portadianteiraesquerda = item.lataria_portadianteiraesquerda
                checklist.lataria_portatraseiradireita = item.lataria_portatraseiradireita
                checklist.lataria_portatraseiraesquerda = item.lataria_portatraseiraesquerda
                checklist.lataria_portamalas = item.lataria_portamalas
                checklist.lataria_parachoquedianteiro = item.lataria_parachoquedianteiro
                checklist.lataria_parachoquetraseiro = item.lataria_parachoquetraseiro
                checklist.lataria_capo = item.lataria_capo
                checklist.lataria_teto = item.lataria_teto
                checklist.eletrica_farolete = item.eletrica_farolete
                checklist.eletrica_farolbaixo = item.eletrica_farolbaixo
                checklist.eletrica_farolalto = item.eletrica_farolalto
                checklist.eletrica_setas = item.eletrica_setas
                checklist.eletrica_luzesdopainel = item.eletrica_luzesdopainel
                checklist.eletrica_luzesinternas = item.eletrica_luzesinternas
                checklist.eletrica_bateria = item.eletrica_bateria
                checklist.eletrica_radio = item.eletrica_radio
                checklist.eletrica_altofalantes = item.eletrica_altofalantes
                checklist.eletrica_limpadorparabrisa = item.eletrica_limpadorparabrisa
                checklist.eletrica_arcondicionado = item.eletrica_arcondicionado
                checklist.eletrica_travas = item.eletrica_travas
                checklist.eletrica_vidros = item.eletrica_vidros
                checklist.vidros_parabrisa = item.vidros_parabrisa
                checklist.vidros_lateraisesquerdo = item.vidros_lateraisesquerdo
                checklist.vidros_lateraisdireito = item.vidros_lateraisdireito
                checklist.vidros_traseiro = item.vidros_traseiro
                checklist.seguranca_triangulo = item.seguranca_triangulo
                checklist.seguranca_extintor = item.seguranca_extintor
                checklist.seguranca_cintos = item.seguranca_cintos
                checklist.seguranca_alarme = item.seguranca_alarme
                checklist.seguranca_fechaduras = item.seguranca_fechaduras
                checklist.seguranca_macanetas = item.seguranca_macanetas
                checklist.seguranca_retrovisores = item.seguranca_retrovisores
                checklist.seguranca_macaco = item.seguranca_macaco
                checklist.pneus_dianteiroesquerdo = item.pneus_dianteiroesquerdo
                checklist.pneus_dianteirodireito = item.pneus_dianteirodireito
                checklist.pneus_traseiroesquerdo = item.pneus_traseiroesquerdo
                checklist.pneus_traseirodireito = item.pneus_traseirodireito
                checklist.pneus_estepe = item.pneus_estepe
                checklist.higienizacao_externa = item.higienizacao_externa
                checklist.higienizacao_interna = item.higienizacao_interna

                session.add(checklist)

                if(item.nome_falcao):
                    session.add(
                        IdentificacaoFalcao(
                            checklist,
                            item.nome_falcao
                        )
                    )

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
                textLogger.log('Checklist - ' + str(e))
                buff.pop(buff.index(item))
                return ConversationHandler.END

            buff.pop(buff.index(item))

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Caso queira relatar um feedback(sugestões, criticas, etc) acesse https://forms.gle/UEYmho6UTU9wHgyD9')

            local_path = 'media/CHECKLIST-' + \
                datetime.now(timezone('America/Sao_Paulo')
                             ).strftime('%b-%Y') + '.xlsx'
            register_now = datetime.now(timezone('America/Sao_Paulo'))

            range_intervalo = CalendarUtils.getRangeByMonthUm(
                register_now.month, register_now.year)

            Session = Database.Session
            session = Session()

            checklists = session.query(Checklist).filter(
                Checklist.dt_abertura >= range_intervalo[0],
                Checklist.dt_abertura < range_intervalo[1]
            ).order_by(Checklist.id.asc())

            try:
                workbook = xlsxwriter.Workbook(local_path)
                worksheet = workbook.add_worksheet()

                row = 0
                col = 0

                worksheet.write(row, col + 0, 'ID')
                worksheet.write(row, col + 1, 'ABERTURA')
                worksheet.write(row, col + 2, 'DATA ABERTURA')
                worksheet.write(row, col + 3, 'HORA ABERTURA')
                worksheet.write(row, col + 4, 'DATA FECHAMENTO')
                
                worksheet.write(row, col + 5, 'HORA FECHAMENTO')
                worksheet.write(row, col + 6, 'PLACA')
                worksheet.write(row, col + 7, 'MOTORISTA')
                worksheet.write(row, col + 8, 'KM INICIAL')
                worksheet.write(row, col + 9, 'KM FINAL')
                worksheet.write(row, col + 10, 'carro_p_casa')
                worksheet.write(row, col + 11, 'viajou_c_carro')
                worksheet.write(row, col + 12, 'manual')
                worksheet.write(row, col + 13, 'crlv')
                worksheet.write(row, col + 14, 'motivo')
                worksheet.write(row, col + 15, 'chave_reserva')
                worksheet.write(row, col + 16, 'outro_condutor')
                worksheet.write(row, col + 17, 'novo_condutor')
                worksheet.write(row, col + 18, 'deixou_oficina')
                worksheet.write(row, col + 19, 'local_oficina')
                worksheet.write(row, col + 20, 'van_tacografo')
                worksheet.write(row, col + 21, 'calibrou_pneu')
                worksheet.write(row, col + 22, 'mecanica_motor')
                worksheet.write(row, col + 23, 'mecanica_amortecedor')
                worksheet.write(row, col + 24, 'mecanica_escapamento')
                worksheet.write(row, col + 25, 'mecanica_freio')
                worksheet.write(row, col + 26, 'mecanica_embreagem')
                worksheet.write(row, col + 27, 'mecanica_acelerador')
                worksheet.write(row, col + 28, 'mecanica_cambio')
                worksheet.write(row, col + 29, 'mecanica_oleo')
                worksheet.write(row, col + 30, 'mecanica_agua')
                worksheet.write(row, col + 31, 'mecanica_alinhamento')
                worksheet.write(row, col + 32, 'mecanica_freiodemao')
                worksheet.write(row, col + 33, 'lataria_dianteiro')
                worksheet.write(row, col + 34, 'lataria_traseiro')
                worksheet.write(row, col + 35, 'lataria_portadianteiradireita')
                worksheet.write(row, col + 36, 'lataria_portadianteiraesquerda')
                worksheet.write(row, col + 37, 'lataria_portatraseiradireita')
                worksheet.write(row, col + 38, 'lataria_portatraseiraesquerda')
                worksheet.write(row, col + 39, 'lataria_portamalas')
                worksheet.write(row, col + 40, 'lataria_parachoquedianteiro')
                worksheet.write(row, col + 41, 'lataria_parachoquetraseiro')
                worksheet.write(row, col + 42, 'lataria_capo')
                worksheet.write(row, col + 43, 'lataria_teto')
                worksheet.write(row, col + 44, 'eletrica_farolete')
                worksheet.write(row, col + 45, 'eletrica_farolbaixo')
                worksheet.write(row, col + 46, 'eletrica_farolalto')
                worksheet.write(row, col + 47, 'eletrica_setas')
                worksheet.write(row, col + 48, 'eletrica_luzesdopainel')
                worksheet.write(row, col + 49, 'eletrica_luzesinternas')
                worksheet.write(row, col + 50, 'eletrica_bateria')
                worksheet.write(row, col + 51, 'eletrica_radio')
                worksheet.write(row, col + 52, 'eletrica_altofalantes')
                worksheet.write(row, col + 53, 'eletrica_limpadorparabrisa')
                worksheet.write(row, col + 54, 'eletrica_arcondicionado')
                worksheet.write(row, col + 55, 'eletrica_travas')
                worksheet.write(row, col + 56, 'eletrica_vidros')
                worksheet.write(row, col + 57, 'vidros_parabrisa')
                worksheet.write(row, col + 58, 'vidros_lateraisesquerdo')
                worksheet.write(row, col + 59, 'vidros_lateraisdireito')
                worksheet.write(row, col + 60, 'vidros_traseiro')
                worksheet.write(row, col + 61, 'seguranca_triangulo')
                worksheet.write(row, col + 62, 'seguranca_extintor')
                worksheet.write(row, col + 63, 'seguranca_cintos')
                worksheet.write(row, col + 64, 'seguranca_alarme')
                worksheet.write(row, col + 65, 'seguranca_fechaduras')
                worksheet.write(row, col + 66, 'seguranca_macanetas')
                worksheet.write(row, col + 67, 'seguranca_retrovisores')
                worksheet.write(row, col + 68, 'seguranca_macaco')
                worksheet.write(row, col + 69, 'pneus_dianteiroesquerdo')
                worksheet.write(row, col + 70, 'pneus_dianteirodireito')
                worksheet.write(row, col + 71, 'pneus_traseiroesquerdo')
                worksheet.write(row, col + 72, 'pneus_traseirodireito')
                worksheet.write(row, col + 72, 'pneus_estepe')
                worksheet.write(row, col + 73, 'higienizacao_externa')
                worksheet.write(row, col + 74, 'higienizacao_interna')
                
                row += 1

                for registro in checklists:
                    worksheet.write(row, col + 0, registro.id)
                    worksheet.write(row, col + 1, registro.is_abertura)
                    worksheet.write(row, col + 2, str(registro.dt_abertura.astimezone(timezone('America/Sao_Paulo')).day) + '/'
                                    + str(registro.dt_abertura.astimezone(timezone('America/Sao_Paulo')).month)
                                    + '/' + str(registro.dt_abertura.astimezone(timezone('America/Sao_Paulo')).year))
                    worksheet.write(row, col + 3, registro.dt_abertura.astimezone(
                        timezone('America/Sao_Paulo')).strftime('%H:%M'))
                    if(registro.dt_fechamento):
                        worksheet.write(row, col + 4, str(registro.dt_fechamento.astimezone(timezone('America/Sao_Paulo')).day) + '/'
                                        + str(registro.dt_fechamento.astimezone(timezone('America/Sao_Paulo')).month)
                                        + '/' + str(registro.dt_fechamento.astimezone(timezone('America/Sao_Paulo')).year))
                        worksheet.write(row, col + 5, registro.dt_fechamento.astimezone(
                            timezone('America/Sao_Paulo')).strftime('%H:%M'))
                    worksheet.write(row, col + 6, registro.placa)
                    worksheet.write(row, col + 7, registro.motorista.nome)
                    worksheet.write(
                        row, col + 8, registro.km_inicial.replace(' KM', ''))
                    worksheet.write(
                        row, col + 9, registro.km_final.replace(' KM', ''))
                    worksheet.write(row, col + 10, registro.carro_p_casa)
                    worksheet.write(row, col + 11, registro.viajou_c_carro)
                    worksheet.write(row, col + 12, registro.manual)
                    worksheet.write(row, col + 13, registro.crlv)
                    worksheet.write(row, col + 14, registro.motivo)
                    worksheet.write(row, col + 15, registro.chave_reserva)
                    worksheet.write(row, col + 16, registro.outro_condutor)
                    worksheet.write(row, col + 17, registro.novo_condutor)
                    worksheet.write(row, col + 18, registro.deixou_oficina)
                    worksheet.write(row, col + 19, registro.local_oficina)
                    worksheet.write(row, col + 20, registro.van_tacografo)
                    worksheet.write(row, col + 21, registro.calibrou_pneu)
                    worksheet.write(row, col + 22, registro.mecanica_motor)
                    worksheet.write(row, col + 23, registro.mecanica_amortecedor)
                    worksheet.write(row, col + 24, registro.mecanica_escapamento)
                    worksheet.write(row, col + 25, registro.mecanica_freio)
                    worksheet.write(row, col + 26, registro.mecanica_embreagem)
                    worksheet.write(row, col + 27, registro.mecanica_acelerador)
                    worksheet.write(row, col + 28, registro.mecanica_cambio)
                    worksheet.write(row, col + 29, registro.mecanica_oleo)
                    worksheet.write(row, col + 30, registro.mecanica_agua)
                    worksheet.write(row, col + 31, registro.mecanica_alinhamento)
                    worksheet.write(row, col + 32, registro.mecanica_freiodemao)
                    worksheet.write(row, col + 33, registro.lataria_dianteiro)
                    worksheet.write(row, col + 34, registro.lataria_traseiro)
                    worksheet.write(row, col + 35, registro.lataria_portadianteiradireita)
                    worksheet.write(row, col + 36, registro.lataria_portadianteiraesquerda)
                    worksheet.write(row, col + 37, registro.lataria_portatraseiradireita)
                    worksheet.write(row, col + 38, registro.lataria_portatraseiraesquerda)
                    worksheet.write(row, col + 39, registro.lataria_portamalas)
                    worksheet.write(row, col + 40, registro.lataria_parachoquedianteiro)
                    worksheet.write(row, col + 41, registro.lataria_parachoquetraseiro)
                    worksheet.write(row, col + 42, registro.lataria_capo)
                    worksheet.write(row, col + 43, registro.lataria_teto)
                    worksheet.write(row, col + 44, registro.eletrica_farolete)
                    worksheet.write(row, col + 45, registro.eletrica_farolbaixo)
                    worksheet.write(row, col + 46, registro.eletrica_farolalto)
                    worksheet.write(row, col + 47, registro.eletrica_setas)
                    worksheet.write(row, col + 48, registro.eletrica_luzesdopainel)
                    worksheet.write(row, col + 49, registro.eletrica_luzesinternas)
                    worksheet.write(row, col + 50, registro.eletrica_bateria)
                    worksheet.write(row, col + 51, registro.eletrica_radio)
                    worksheet.write(row, col + 52, registro.eletrica_altofalantes)
                    worksheet.write(row, col + 53, registro.eletrica_limpadorparabrisa)
                    worksheet.write(row, col + 54, registro.eletrica_arcondicionado)
                    worksheet.write(row, col + 55, registro.eletrica_travas)
                    worksheet.write(row, col + 56, registro.eletrica_vidros)
                    worksheet.write(row, col + 57, registro.vidros_parabrisa)
                    worksheet.write(row, col + 58, registro.vidros_lateraisesquerdo)
                    worksheet.write(row, col + 59, registro.vidros_lateraisdireito)
                    worksheet.write(row, col + 60, registro.vidros_traseiro)
                    worksheet.write(row, col + 61, registro.seguranca_triangulo)
                    worksheet.write(row, col + 62, registro.seguranca_extintor)
                    worksheet.write(row, col + 63, registro.seguranca_cintos)
                    worksheet.write(row, col + 64, registro.seguranca_alarme)
                    worksheet.write(row, col + 65, registro.seguranca_fechaduras)
                    worksheet.write(row, col + 66, registro.seguranca_macanetas)
                    worksheet.write(row, col + 67, registro.seguranca_retrovisores)
                    worksheet.write(row, col + 68, registro.seguranca_macaco)
                    worksheet.write(row, col + 69, registro.pneus_dianteiroesquerdo)
                    worksheet.write(row, col + 70, registro.pneus_dianteirodireito)
                    worksheet.write(row, col + 71, registro.pneus_traseiroesquerdo)
                    worksheet.write(row, col + 72, registro.pneus_traseirodireito)
                    worksheet.write(row, col + 72, registro.pneus_estepe)
                    worksheet.write(row, col + 73, registro.higienizacao_externa)
                    worksheet.write(row, col + 74, registro.higienizacao_interna)
                    row += 1

                workbook.close()

            except Exception as e:
                print(e)

            session.close()
            gdrive.upload_gdrive(local_path, local_path.replace('media/', ''))
            os.remove(local_path)

            return ConversationHandler.END
        elif(update.message.text == 'Não, refazer'):
            update.message.reply_text(
                'Ok! Vamos refazer então. Motorista, informe o KM inicial',
                one_time_keyboard=True)

            return KM_INICIAL
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            update.message.reply_text(
                'Opção inválida, por favor responda apenas: "Sim, confirmar", "Não, refazer" ou "Cancelar".',
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard2, one_time_keyboard=True)
            )

            return F_CONFIRM

    def fechar_checklist(self, update, context):
        if update.callback_query:
            try:
                current_chat_id = update.callback_query.message.chat.id
                current_username = update.callback_query.from_user.username
                open_checklist = RegChecklist(
                    current_username, current_chat_id, False)
            except Exception as e:
                print(e)
                context.bot.send_message(
                    chat_id=current_chat_id,
                    text='Não é possível realizar o cadastro de checklist sem um nome de usuário cadastrado.')
                return ConversationHandler.END
        else:
            try:
                current_chat_id = update.message.chat.id
                current_username = update.message.from_user.username
                open_checklist = RegChecklist(
                    current_username, current_chat_id, False)
            except Exception as e:
                print(e)
                update.message.reply_text(
                    'Não é possível realizar o cadastro de checklist sem um nome de usuário cadastrado.',
                    reply_markup=ReplyKeyboardRemove()
                )
                return ConversationHandler.END

        try:
            Session = Database.Session
            session = Session()

            motorista = session.query(Motorista).filter_by(
                telegram_user=current_username).first()

            if motorista is None:
                context.bot.send_message(
                    chat_id=current_chat_id,
                    text='Usuário ' + current_username + ' não encontrado na base de dados. ' +
                    'Acesso não autorizado!', reply_markup=ReplyKeyboardRemove()
                )
                session.close()
                return ConversationHandler.END
            else:
                checklist = session.query(Checklist).filter_by(
                    motorista_id=motorista.id).order_by(Checklist.id.desc()).first()

            if checklist and not checklist.dt_fechamento:
                open_checklist.idd = checklist.id
                open_checklist.motorista_id = checklist.motorista_id
                open_checklist.placa = checklist.placa
                open_checklist.km_inicial = checklist.km_inicial
                open_checklist.dt_abertura = checklist.dt_abertura

                buff.append(open_checklist)
            else:
                context.bot.send_message(
                    chat_id=current_chat_id,
                    text='Não foi possível fechar um checklist.\n\n*MOTIVO: não existe um checklist em aberto*\n',
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode=ParseMode.MARKDOWN
                )
                session.close()
                return ConversationHandler.END

            session.close()
        except:
            context.bot.send_message(
                chat_id=current_chat_id,
                text='Houve um erro ao tentar se conectar com a base de dados! ' +
                     'O erro foi reportado, tente novamente mais tarde.',
                     reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        context.bot.send_message(
            chat_id=current_chat_id,
            text='Olá, ' + motorista.nome + '. Por favor, informe a quilometragem final.', reply_markup=ReplyKeyboardRemove())

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
            'Quilometragem enviada: ' + update.message.text + ' KM\n\n' +
            'A quilometragem foi inserida corretamente?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return KM_CONFIRM

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

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=str_menu,
            reply_markup=ReplyKeyboardMarkup(keyboardMenu(9))
        )

        return MENU_SWITCHER

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

                motorista = session.query(Motorista).filter_by(
                    telegram_user=item.username).first()

                checklist_abertura = session.query(Checklist).filter_by(
                    motorista_id=motorista.id).order_by(Checklist.id.desc()).first()

                checklist = Checklist(
                    motorista,
                    False,
                    item.placa,
                    str(item.km_inicial),
                    item.dt_abertura
                )

                checklist.km_final = str(item.km_final) + ' KM'
                checklist.dt_fechamento = datetime.now(
                    timezone('America/Sao_Paulo'))

                checklist_abertura.dt_fechamento = checklist.dt_fechamento

                checklist.carro_p_casa = item.carro_p_casa
                checklist.viajou_c_carro = item.viajou_c_carro
                checklist.manual = item.manual
                checklist.crlv = item.crlv
                checklist.motivo = item.motivo
                checklist.chave_reserva = item.chave_reserva
                checklist.outro_condutor = item.outro_condutor
                checklist.novo_condutor = item.novo_condutor
                checklist.deixou_oficina = item.deixou_oficina
                checklist.local_oficina = item.local_oficina
                checklist.van_tacografo = item.van_tacografo
                checklist.calibrou_pneu = item.calibrou_pneu
                checklist.mecanica_motor = item.mecanica_motor
                checklist.mecanica_amortecedor = item.mecanica_amortecedor
                checklist.mecanica_escapamento = item.mecanica_escapamento
                checklist.mecanica_freio = item.mecanica_freio
                checklist.mecanica_embreagem = item.mecanica_embreagem
                checklist.mecanica_acelerador = item.mecanica_acelerador
                checklist.mecanica_cambio = item.mecanica_cambio
                checklist.mecanica_oleo = item.mecanica_oleo
                checklist.mecanica_agua = item.mecanica_agua
                checklist.mecanica_alinhamento = item.mecanica_alinhamento
                checklist.mecanica_freiodemao = item.mecanica_freiodemao
                checklist.lataria_dianteiro = item.lataria_dianteiro
                checklist.lataria_traseiro = item.lataria_traseiro
                checklist.lataria_portadianteiradireita = item.lataria_portadianteiradireita
                checklist.lataria_portadianteiraesquerda = item.lataria_portadianteiraesquerda
                checklist.lataria_portatraseiradireita = item.lataria_portatraseiradireita
                checklist.lataria_portatraseiraesquerda = item.lataria_portatraseiraesquerda
                checklist.lataria_portamalas = item.lataria_portamalas
                checklist.lataria_parachoquedianteiro = item.lataria_parachoquedianteiro
                checklist.lataria_parachoquetraseiro = item.lataria_parachoquetraseiro
                checklist.lataria_capo = item.lataria_capo
                checklist.lataria_teto = item.lataria_teto
                checklist.eletrica_farolete = item.eletrica_farolete
                checklist.eletrica_farolbaixo = item.eletrica_farolbaixo
                checklist.eletrica_farolalto = item.eletrica_farolalto
                checklist.eletrica_setas = item.eletrica_setas
                checklist.eletrica_luzesdopainel = item.eletrica_luzesdopainel
                checklist.eletrica_luzesinternas = item.eletrica_luzesinternas
                checklist.eletrica_bateria = item.eletrica_bateria
                checklist.eletrica_radio = item.eletrica_radio
                checklist.eletrica_altofalantes = item.eletrica_altofalantes
                checklist.eletrica_limpadorparabrisa = item.eletrica_limpadorparabrisa
                checklist.eletrica_arcondicionado = item.eletrica_arcondicionado
                checklist.eletrica_travas = item.eletrica_travas
                checklist.eletrica_vidros = item.eletrica_vidros
                checklist.vidros_parabrisa = item.vidros_parabrisa
                checklist.vidros_lateraisesquerdo = item.vidros_lateraisesquerdo
                checklist.vidros_lateraisdireito = item.vidros_lateraisdireito
                checklist.vidros_traseiro = item.vidros_traseiro
                checklist.seguranca_triangulo = item.seguranca_triangulo
                checklist.seguranca_extintor = item.seguranca_extintor
                checklist.seguranca_cintos = item.seguranca_cintos
                checklist.seguranca_alarme = item.seguranca_alarme
                checklist.seguranca_fechaduras = item.seguranca_fechaduras
                checklist.seguranca_macanetas = item.seguranca_macanetas
                checklist.seguranca_retrovisores = item.seguranca_retrovisores
                checklist.seguranca_macaco = item.seguranca_macaco
                checklist.pneus_dianteiroesquerdo = item.pneus_dianteiroesquerdo
                checklist.pneus_dianteirodireito = item.pneus_dianteirodireito
                checklist.pneus_traseiroesquerdo = item.pneus_traseiroesquerdo
                checklist.pneus_traseirodireito = item.pneus_traseirodireito
                checklist.pneus_estepe = item.pneus_estepe
                checklist.higienizacao_externa = item.higienizacao_externa
                checklist.higienizacao_interna = item.higienizacao_interna

                session.add(checklist_abertura)
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
                textLogger.log('Checklist - ' + str(e))
                buff.pop(buff.index(item))
                return ConversationHandler.END

            buff.pop(buff.index(item))

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Caso queira relatar um feedback(sugestões, criticas, etc) acesse https://forms.gle/UEYmho6UTU9wHgyD9')

            local_path = 'media/CHECKLIST-' + \
                datetime.now(timezone('America/Sao_Paulo')
                             ).strftime('%b-%Y') + '.xlsx'
            register_now = datetime.now(timezone('America/Sao_Paulo'))

            range_intervalo = CalendarUtils.getRangeByMonthUm(
                register_now.month, register_now.year)

            Session = Database.Session
            session = Session()

            checklists = session.query(Checklist).filter(
                Checklist.dt_abertura >= range_intervalo[0],
                Checklist.dt_abertura < range_intervalo[1]
            ).order_by(Checklist.id.asc())

            try:
                workbook = xlsxwriter.Workbook(local_path)
                worksheet = workbook.add_worksheet()

                row = 0
                col = 0

                worksheet.write(row, col + 0, 'ID')
                worksheet.write(row, col + 1, 'ABERTURA')
                worksheet.write(row, col + 2, 'DATA ABERTURA')
                worksheet.write(row, col + 3, 'HORA ABERTURA')
                worksheet.write(row, col + 4, 'DATA FECHAMENTO')
                worksheet.write(row, col + 5, 'HORA FECHAMENTO')
                worksheet.write(row, col + 6, 'PLACA')
                worksheet.write(row, col + 7, 'NOME')
                worksheet.write(row, col + 8, 'KM INICIAL')
                worksheet.write(row, col + 9, 'KM FINAL')

                row += 1

                for registro in checklists:
                    worksheet.write(row, col + 0, registro.id)
                    worksheet.write(row, col + 1, registro.is_abertura)
                    worksheet.write(row, col + 2, str(registro.dt_abertura.astimezone(timezone('America/Sao_Paulo')).day) + '/'
                                    + str(registro.dt_abertura.astimezone(timezone('America/Sao_Paulo')).month)
                                    + '/' + str(registro.dt_abertura.astimezone(timezone('America/Sao_Paulo')).year))
                    worksheet.write(row, col + 3, registro.dt_abertura.astimezone(
                        timezone('America/Sao_Paulo')).strftime('%H:%M'))
                    if(registro.dt_fechamento):
                        worksheet.write(row, col + 4, str(registro.dt_fechamento.astimezone(timezone('America/Sao_Paulo')).day) + '/'
                                        + str(registro.dt_fechamento.astimezone(timezone('America/Sao_Paulo')).month)
                                        + '/' + str(registro.dt_fechamento.astimezone(timezone('America/Sao_Paulo')).year))
                        worksheet.write(row, col + 5, registro.dt_fechamento.astimezone(
                            timezone('America/Sao_Paulo')).strftime('%H:%M'))
                    worksheet.write(row, col + 6, registro.placa)
                    worksheet.write(row, col + 7, registro.motorista.nome)
                    worksheet.write(
                        row, col + 8, registro.km_inicial.replace(' KM', ''))
                    worksheet.write(
                        row, col + 9, registro.km_final.replace(' KM', ''))
                    row += 1

                workbook.close()

            except Exception as e:
                print(e)

            session.close()
            gdrive.upload_gdrive(local_path, local_path.replace('media/', ''))
            os.remove(local_path)

            return ConversationHandler.END
        elif(update.message.text == 'Não, refazer'):
            update.message.reply_text(
                'Ok! Vamos refazer então. Motorista, informe a KM Final',
                one_time_keyboard=True)

            return KM_FINAL
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            update.message.reply_text(
                'Opção inválida, por favor responda apenas: "Sim, confirmar", "Não, refazer" ou "Cancelar".',
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard2, one_time_keyboard=True)
            )

            return F_CONFIRM

    def cancel(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        buff.pop(buff.index(item))
        user = update.message.from_user
        self.logger.info("Usuario %s cancelou a conversa.", user.first_name)
        update.message.reply_text('Operação cancelada!',
                                  reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def conformidade(self, update, context):
        reply_keyboard = [['Sim, registrar'], ['Não, finalizar'], ['Cancelar']]

        if(update.message.text == 'Sim, registrar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Por favor, envie a foto da ocorrência a ser registrada.')
            return F_CONFORMIDADE
        elif(update.message.text == 'Não, finalizar'):
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]

            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a verificação geral do checklist!')

            try:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosFalse(), parse_mode=ParseMode.MARKDOWN)
            except:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Todos itens do veículo estão ok.", parse_mode=ParseMode.MARKDOWN)

            if(item.is_abertura):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosAbertura(), parse_mode=ParseMode.MARKDOWN)

                update.message.reply_text(
                    'O dados informados estão corretos?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
                return A_CONFIRM
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosFechamento(), parse_mode=ParseMode.MARKDOWN)

                update.message.reply_text(
                    'O dados informados estão corretos?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
                return F_CONFIRM
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!'
            )
            buff.pop(buff.index(item))
            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Por favor, responda apenas: "Sim, registrar", "Não, finalizar" ou "Cancelar"'
            )
            update.message.reply_text(
                'Deseja registrar algo por foto?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return CONFORMIDADE

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
                "Agora envie a foto da ocorrencia."
            )
            listUtils.listItens(buff)
            return F_CONFORMIDADE

        update.message.reply_text(
            "Agora descreva a ocorrência:"
        )

        return O_CONFORMIDADE

    def o_conformidade(self, update, context):

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Salvando a ocorrência...')

        item.desc_conformidades.append(update.message.text)
        aux = item.desc_conformidades

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'desc_conformidades',
                                  aux)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Salvo com sucesso!'
        )

        reply_keyboard = [['Sim, registrar'], ['Não, finalizar'], ['Cancelar']]

        update.message.reply_text(
            'Houve mais alguma ocorrência?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CONFORMIDADE

    def menu_switcher(self, update, context):
        if not update.message.text in valid_in_switcher:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Opção inválida, por favor, responda apenas: " +
                str(valid_in_switcher).replace("'", "")
            )
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=str_menu,
                reply_markup=ReplyKeyboardMarkup(keyboardMenu(9))
            )

            return MENU_SWITCHER

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if update.message.text == '8':
            reply_keyboard2 = [['Sim, registrar'],
                               ['Não, finalizar'], ['Cancelar']]
            update.message.reply_text(
                'Deseja registrar algo por foto?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

            return CONFORMIDADE
        elif update.message.text == '9':
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            received_opt = int(update.message.text)
            for index, a in enumerate(ASSOC.keys()):
                if received_opt == (index + 1):
                    choosed = a
                    break
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'cache_group',
                                      choosed)

            update.message.reply_text(
                dynamic_menu(choosed),
                reply_markup=ReplyKeyboardMarkup(
                    keyboardMenu(len(ASSOC[choosed]))),
                parse_mode=ParseMode.MARKDOWN
            )

            return MENU_DINAMICO

        return ConversationHandler.END

    def menu_dinamico(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        valid = list(
            map(str, list(range(1, len(ASSOC[item.cache_group]) + 1))))

        print(item.cache_id, item.cache_group)

        if item.cache_id > 0 and (not update.message.text in ['Sim, confirmar', 'Não, retornar']):
            selected_item = ASSOC[item.cache_group][item.cache_id]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Opção inválida, por favor, responda apenas: " +
                str(['Sim, confirmar', 'Não, retornar']).replace("'", "")
            )

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Deseja confirmar que o item -> *" +
                selected_item[1] + "* não está ok?",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, retornar']])
            )

            return MENU_DINAMICO

        if (update.message.text == 'Sim, confirmar') and item.cache_id > 0:
            selected_item = ASSOC[item.cache_group][item.cache_id]

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="O item *" + selected_item[1] +
                "* foi registrado como 'NÃO ESTÁ OK'",
                parse_mode=ParseMode.MARKDOWN
            )
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      item.cache_group + '_' +
                                      selected_item[0],
                                      False)
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'cache_id',
                                      -1)
        elif (update.message.text == 'Não, retornar') and item.cache_id > 0:
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'cache_id',
                                      -1)
        elif not update.message.text in valid:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Opção inválida, por favor, responda apenas: " +
                str(valid).replace("'", "")
            )
        else:
            if int(update.message.text) == len(ASSOC[item.cache_group]):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=str_menu,
                    reply_markup=ReplyKeyboardMarkup(keyboardMenu(9))
                )

                return MENU_SWITCHER

            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'cache_id',
                                      int(update.message.text))

            selected_item = ASSOC[item.cache_group][int(update.message.text)]
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Deseja confirmar que o item -> *" +
                selected_item[1] + "* não está ok?",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=ReplyKeyboardMarkup(
                    [['Sim, confirmar'], ['Não, retornar']])
            )

            return MENU_DINAMICO

        update.message.reply_text(
            dynamic_menu(item.cache_group),
            reply_markup=ReplyKeyboardMarkup(
                keyboardMenu(len(ASSOC[item.cache_group]))),
            parse_mode=ParseMode.MARKDOWN
        )

        return MENU_DINAMICO
