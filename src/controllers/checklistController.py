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
from models.Veiculos import Veiculos

from models.regChecklist import RegChecklist

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

LATARIA_DIANTEIRO = 21
LATARIA_TRASEIRO = 22
LATARIA_PORTADIANTEIRADIREITA = 23
LATARIA_PORTADIANTEIRAESQUERDA = 24
LATARIA_PORTATRASEIRADIREITA = 25
LATARIA_PORTATRASEIRAESQUERDA = 26
LATARIA_PORTAMALAS = 27
LATARIA_PARACHOQUEDIANTEIRO = 28
LATARIA_PARACHOQUETRASEIRO = 29
LATARIA_CAPO = 30
LATARIA_TETO = 31
LATARIA_CONFIRM = 32

ELETRICA_FAROLETE = 33
ELETRICA_FAROLBAIXO = 34
ELETRICA_FAROLALTO = 35
ELETRICA_SETAS = 36
ELETRICA_LUZESDOPAINEL = 37
ELETRICA_LUZESINTERNAS = 38
ELETRICA_BATERIA = 39
ELETRICA_RADIO = 40
ELETRICA_ALTOFALANTES = 41
ELETRICA_LIMPADORPARABRISA = 42
ELETRICA_ARCONDICIONADO = 43
ELETRICA_TRAVAS = 44
ELETRICA_VIDROS = 45
ELETRICA_CONFIRM = 46

VIDROS_PARABRISA = 47
VIDROS_LATERAISESQUERDO = 48
VIDROS_LATERAISDIREITO = 49
VIDROS_TRASEIRO = 50
VIDROS_CONFIRM = 51

SEGURANCA_TRIANGULO = 52
SEGURANCA_EXTINTOR = 53
SEGURANCA_CINTOS = 54
SEGURANCA_ALARME = 55
SEGURANCA_FECHADURAS = 56
SEGURANCA_MACANETAS = 57
SEGURANCA_RETROVISORES = 58
SEGURANCA_MACACO = 59
SEGURANCA_CONFIRM = 60

PNEUS_DIANTEIROESQUERDO = 61
PNEUS_DIANTEIRODIREITO = 62
PNEUS_TRASEIROESQUERDO = 63
PNEUS_TRASEIRODIREITO = 64
PNEUS_ESTEPE = 65
PNEUS_CONFIRM = 66

HIGIENIZACAO_EXTERNA = 67
HIGIENIZACAO_INTERNA = 68
HIGIENIZACAO_CONFIRM = 69

F_CONFIRM = 70

CONFORMIDADE = 72
F_CONFORMIDADE = 73
O_CONFORMIDADE = 74

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
                A_CONFIRM: [MessageHandler(Filters.text, self.a_confirm)],
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

                LATARIA_DIANTEIRO: [MessageHandler(Filters.text, self.lataria_dianteiro)],
                LATARIA_TRASEIRO: [MessageHandler(Filters.text, self.lataria_traseiro)],
                LATARIA_PORTADIANTEIRADIREITA: [MessageHandler(Filters.text, self.lataria_portadianteiradireita)],
                LATARIA_PORTADIANTEIRAESQUERDA: [MessageHandler(Filters.text, self.lataria_portadianteiraesquerda)],
                LATARIA_PORTATRASEIRADIREITA: [MessageHandler(Filters.text, self.lataria_portatraseiradireita)],
                LATARIA_PORTATRASEIRAESQUERDA: [MessageHandler(Filters.text, self.lataria_portatraseiraesquerda)],
                LATARIA_PORTAMALAS: [MessageHandler(Filters.text, self.lataria_portamalas)],
                LATARIA_PARACHOQUEDIANTEIRO: [MessageHandler(Filters.text, self.lataria_parachoquedianteiro)],
                LATARIA_PARACHOQUETRASEIRO: [MessageHandler(Filters.text, self.lataria_parachoquetraseiro)],
                LATARIA_CAPO: [MessageHandler(Filters.text, self.lataria_capo)],
                LATARIA_TETO: [MessageHandler(Filters.text, self.lataria_teto)],
                LATARIA_CONFIRM: [MessageHandler(Filters.text, self.lataria_confirm)],

                ELETRICA_FAROLETE: [MessageHandler(Filters.text, self.eletrica_farolete)],
                ELETRICA_FAROLBAIXO: [MessageHandler(Filters.text, self.eletrica_farolbaixo)],
                ELETRICA_FAROLALTO: [MessageHandler(Filters.text, self.eletrica_farolalto)],
                ELETRICA_SETAS: [MessageHandler(Filters.text, self.eletrica_setas)],
                ELETRICA_LUZESDOPAINEL: [MessageHandler(Filters.text, self.eletrica_luzesdopainel)],
                ELETRICA_LUZESINTERNAS: [MessageHandler(Filters.text, self.eletrica_luzesinternas)],
                ELETRICA_BATERIA: [MessageHandler(Filters.text, self.eletrica_bateria)],
                ELETRICA_RADIO: [MessageHandler(Filters.text, self.eletrica_radio)],
                ELETRICA_ALTOFALANTES: [MessageHandler(Filters.text, self.eletrica_altofalantes)],
                ELETRICA_LIMPADORPARABRISA: [MessageHandler(Filters.text, self.eletrica_limpadorparabrisa)],
                ELETRICA_ARCONDICIONADO: [MessageHandler(Filters.text, self.eletrica_arcondicionado)],
                ELETRICA_TRAVAS: [MessageHandler(Filters.text, self.eletrica_travas)],
                ELETRICA_VIDROS: [MessageHandler(Filters.text, self.eletrica_vidros)],
                ELETRICA_CONFIRM: [MessageHandler(Filters.text, self.eletrica_confirm)],

                VIDROS_PARABRISA: [MessageHandler(Filters.text, self.vidros_parabrisa)],
                VIDROS_LATERAISESQUERDO: [MessageHandler(Filters.text, self.vidros_lateraisesquerdo)],
                VIDROS_LATERAISDIREITO: [MessageHandler(Filters.text, self.vidros_lateraisdireito)],
                VIDROS_TRASEIRO: [MessageHandler(Filters.text, self.vidros_traseiro)],
                VIDROS_CONFIRM: [MessageHandler(Filters.text, self.vidros_confirm)],

                SEGURANCA_TRIANGULO: [MessageHandler(Filters.text, self.seguranca_triangulo)],
                SEGURANCA_EXTINTOR: [MessageHandler(Filters.text, self.seguranca_extintor)],
                SEGURANCA_CINTOS: [MessageHandler(Filters.text, self.seguranca_cintos)],
                SEGURANCA_ALARME: [MessageHandler(Filters.text, self.seguranca_alarme)],
                SEGURANCA_FECHADURAS: [MessageHandler(Filters.text, self.seguranca_fechaduras)],
                SEGURANCA_MACANETAS: [MessageHandler(Filters.text, self.seguranca_macanetas)],
                SEGURANCA_RETROVISORES: [MessageHandler(Filters.text, self.seguranca_retrovisores)],
                SEGURANCA_MACACO: [MessageHandler(Filters.text, self.seguranca_macaco)],
                SEGURANCA_CONFIRM: [MessageHandler(Filters.text, self.seguranca_confirm)],

                PNEUS_DIANTEIROESQUERDO: [MessageHandler(Filters.text, self.pneus_dianteiroesquerdo)],
                PNEUS_DIANTEIRODIREITO: [MessageHandler(Filters.text, self.pneus_dianteirodireito)],
                PNEUS_TRASEIROESQUERDO: [MessageHandler(Filters.text, self.pneus_traseiroesquerdo)],
                PNEUS_TRASEIRODIREITO: [MessageHandler(Filters.text, self.pneus_traseirodireito)],
                PNEUS_ESTEPE: [MessageHandler(Filters.text, self.pneus_estepe)],
                PNEUS_CONFIRM: [MessageHandler(Filters.text, self.pneus_confirm)],

                HIGIENIZACAO_EXTERNA: [MessageHandler(Filters.text, self.higienizacao_externa)],
                HIGIENIZACAO_INTERNA: [MessageHandler(Filters.text, self.higienizacao_interna)],
                HIGIENIZACAO_CONFIRM: [MessageHandler(Filters.text, self.higienizacao_confirm)],

                CONFORMIDADE: [MessageHandler(Filters.text, self.conformidade)],
                F_CONFORMIDADE: [MessageHandler(Filters.photo, self.f_conformidade)],
                O_CONFORMIDADE: [MessageHandler(
                    Filters.text, self.o_conformidade)]

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

                LATARIA_DIANTEIRO: [MessageHandler(Filters.text, self.lataria_dianteiro)],
                LATARIA_TRASEIRO: [MessageHandler(Filters.text, self.lataria_traseiro)],
                LATARIA_PORTADIANTEIRADIREITA: [MessageHandler(Filters.text, self.lataria_portadianteiradireita)],
                LATARIA_PORTADIANTEIRAESQUERDA: [MessageHandler(Filters.text, self.lataria_portadianteiraesquerda)],
                LATARIA_PORTATRASEIRADIREITA: [MessageHandler(Filters.text, self.lataria_portatraseiradireita)],
                LATARIA_PORTATRASEIRAESQUERDA: [MessageHandler(Filters.text, self.lataria_portatraseiraesquerda)],
                LATARIA_PORTAMALAS: [MessageHandler(Filters.text, self.lataria_portamalas)],
                LATARIA_PARACHOQUEDIANTEIRO: [MessageHandler(Filters.text, self.lataria_parachoquedianteiro)],
                LATARIA_PARACHOQUETRASEIRO: [MessageHandler(Filters.text, self.lataria_parachoquetraseiro)],
                LATARIA_CAPO: [MessageHandler(Filters.text, self.lataria_capo)],
                LATARIA_TETO: [MessageHandler(Filters.text, self.lataria_teto)],
                LATARIA_CONFIRM: [MessageHandler(Filters.text, self.lataria_confirm)],

                ELETRICA_FAROLETE: [MessageHandler(Filters.text, self.eletrica_farolete)],
                ELETRICA_FAROLBAIXO: [MessageHandler(Filters.text, self.eletrica_farolbaixo)],
                ELETRICA_FAROLALTO: [MessageHandler(Filters.text, self.eletrica_farolalto)],
                ELETRICA_SETAS: [MessageHandler(Filters.text, self.eletrica_setas)],
                ELETRICA_LUZESDOPAINEL: [MessageHandler(Filters.text, self.eletrica_luzesdopainel)],
                ELETRICA_LUZESINTERNAS: [MessageHandler(Filters.text, self.eletrica_luzesinternas)],
                ELETRICA_BATERIA: [MessageHandler(Filters.text, self.eletrica_bateria)],
                ELETRICA_RADIO: [MessageHandler(Filters.text, self.eletrica_radio)],
                ELETRICA_ALTOFALANTES: [MessageHandler(Filters.text, self.eletrica_altofalantes)],
                ELETRICA_LIMPADORPARABRISA: [MessageHandler(Filters.text, self.eletrica_limpadorparabrisa)],
                ELETRICA_ARCONDICIONADO: [MessageHandler(Filters.text, self.eletrica_arcondicionado)],
                ELETRICA_TRAVAS: [MessageHandler(Filters.text, self.eletrica_travas)],
                ELETRICA_VIDROS: [MessageHandler(Filters.text, self.eletrica_vidros)],
                ELETRICA_CONFIRM: [MessageHandler(Filters.text, self.eletrica_confirm)],

                VIDROS_PARABRISA: [MessageHandler(Filters.text, self.vidros_parabrisa)],
                VIDROS_LATERAISESQUERDO: [MessageHandler(Filters.text, self.vidros_lateraisesquerdo)],
                VIDROS_LATERAISDIREITO: [MessageHandler(Filters.text, self.vidros_lateraisdireito)],
                VIDROS_TRASEIRO: [MessageHandler(Filters.text, self.vidros_traseiro)],
                VIDROS_CONFIRM: [MessageHandler(Filters.text, self.vidros_confirm)],

                SEGURANCA_TRIANGULO: [MessageHandler(Filters.text, self.seguranca_triangulo)],
                SEGURANCA_EXTINTOR: [MessageHandler(Filters.text, self.seguranca_extintor)],
                SEGURANCA_CINTOS: [MessageHandler(Filters.text, self.seguranca_cintos)],
                SEGURANCA_ALARME: [MessageHandler(Filters.text, self.seguranca_alarme)],
                SEGURANCA_FECHADURAS: [MessageHandler(Filters.text, self.seguranca_fechaduras)],
                SEGURANCA_MACANETAS: [MessageHandler(Filters.text, self.seguranca_macanetas)],
                SEGURANCA_RETROVISORES: [MessageHandler(Filters.text, self.seguranca_retrovisores)],
                SEGURANCA_MACACO: [MessageHandler(Filters.text, self.seguranca_macaco)],
                SEGURANCA_CONFIRM: [MessageHandler(Filters.text, self.seguranca_confirm)],

                PNEUS_DIANTEIROESQUERDO: [MessageHandler(Filters.text, self.pneus_dianteiroesquerdo)],
                PNEUS_DIANTEIRODIREITO: [MessageHandler(Filters.text, self.pneus_dianteirodireito)],
                PNEUS_TRASEIROESQUERDO: [MessageHandler(Filters.text, self.pneus_traseiroesquerdo)],
                PNEUS_TRASEIRODIREITO: [MessageHandler(Filters.text, self.pneus_traseirodireito)],
                PNEUS_ESTEPE: [MessageHandler(Filters.text, self.pneus_estepe)],
                PNEUS_CONFIRM: [MessageHandler(Filters.text, self.pneus_confirm)],

                HIGIENIZACAO_EXTERNA: [MessageHandler(Filters.text, self.higienizacao_externa)],
                HIGIENIZACAO_INTERNA: [MessageHandler(Filters.text, self.higienizacao_interna)],
                HIGIENIZACAO_CONFIRM: [MessageHandler(Filters.text, self.higienizacao_confirm)],

                F_CONFIRM: [MessageHandler(Filters.text, self.f_confirm)],

                CONFORMIDADE: [MessageHandler(Filters.text, self.conformidade)],
                F_CONFORMIDADE: [MessageHandler(Filters.photo, self.f_conformidade)],
                O_CONFORMIDADE: [MessageHandler(
                    Filters.text, self.o_conformidade)]
            },

            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

    def abrir_checklist(self, update, context):
        placas = []

        try:
            open_checklist = RegChecklist(
                update.message.from_user.username, update.message.chat.id, True)
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
                session.close()
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
                session.close()
                return ConversationHandler.END

            veiculos = session.query(Veiculos).order_by(Veiculos.placa.asc())

            for veiculo in veiculos:
                placas.append([veiculo.placa])

            session.close()
        except:
            update.message.reply_text('Houve um erro ao tentar se conectar com a base de dados! ' +
                                      'O erro foi reportado, tente novamente mais tarde.',
                                      reply_markup=ReplyKeyboardRemove())
            return ConversationHandler.END

        update.message.reply_text(
            'Olá, ' + motorista.nome + '. Por favor, informe a placa do veículo.',
            reply_markup=ReplyKeyboardMarkup(placas, one_time_keyboard=True))

        return PLACA

    def placa(self, update, context):
        user = update.message.from_user

        Session = Database.Session
        session = Session()

        placa = session.query(Veiculos).filter_by(
            placa=update.message.text).first()

        if placa is None:
            placas = []
            veiculos = session.query(Veiculos).order_by(Veiculos.placa.asc())

            for veiculo in veiculos:
                placas.append([veiculo.placa])

            update.message.reply_text(
                'Placa ' + update.message.text + ' inválida ou não encontrada na base de dados. ' +
                'Por favor, informe novamente a placa do veículo.',
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

        # item = listUtils.searchAndGetItem(buff,
        #                                   update.message.from_user.username,
        #                                   update.message.chat.id)

        # update.message.reply_text(
        #     item.dadosAbertura(), parse_mode=ParseMode.MARKDOWN)

        # reply_keyboard = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]

        # update.message.reply_text(
        #     'O dados informados estão corretos?',
        #     reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        # return A_CONFIRM

        reply_keyboard = [['Sim'], ['Não']]

        update.message.reply_text(
            'Retornou com o carro para casa?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CARRO_P_CASA

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
                    item.dt_abertura
                )

                checklist.carro_p_casa = item.carro_p_casa
                checklist.viajou_c_carro = item.viajou_c_carro
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
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
            )

            return F_CONFIRM

    def fechar_checklist(self, update, context):
        try:
            open_checklist = RegChecklist(
                update.message.from_user.username, update.message.chat.id, False)
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

                buff.append(open_checklist)
            else:
                update.message.reply_text(
                    'Não foi possível fechar um checklist.\n\n*MOTIVO: não existe um checklist em aberto*\n',
                    reply_markup=ReplyKeyboardRemove(),
                    parse_mode=ParseMode.MARKDOWN
                )
                session.close()
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
        # item = listUtils.searchAndGetItem(buff,
        #                                  update.message.from_user.username,
        #                                  update.message.chat.id)
        # update.message.reply_text(
        #    item.dadosFechamento(), parse_mode=ParseMode.MARKDOWN)
        # update.message.reply_text(
        #    'O dados informados estão corretos?',
        #    reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        # return F_CONFIRM

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
            'Como está o freio?',
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
            'Como está o acelerador?',
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
                'Como está a lataria dianteira?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return LATARIA_DIANTEIRO
        elif(update.message.text == 'Não, refazer'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos novamente a revisão da mecanica do veículo!')

            update.message.reply_text(
                'Como está o motor?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return MECANICA_MOTOR
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Opção invalida. Por favor, responda apenas: [Sim, confirmar], [Não, refazer] ou [Cancelar]')
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            update.message.reply_text(
                item.dadosMecanica(), parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(
                'O dados informados estão corretos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

    def lataria_dianteiro(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_dianteiro',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_dianteiro',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a lataria dianteira?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return LATARIA_DIANTEIRO

        update.message.reply_text(
            'Como está a lataria traseira?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return LATARIA_TRASEIRO

    def lataria_traseiro(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_traseiro',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_traseiro',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a lataria traseira?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_TRASEIRO
        update.message.reply_text(
            'Como está a porta dianteira direita?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_PORTADIANTEIRADIREITA

    def lataria_portadianteiradireita(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portadianteiradireita',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portadianteiradireita',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a porta dianteira direita?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_PORTADIANTEIRADIREITA
        update.message.reply_text(
            'Como está a porta dianteira esquerda?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_PORTADIANTEIRAESQUERDA

    def lataria_portadianteiraesquerda(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portadianteiraesquerda',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portadianteiraesquerda',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a porta dianteira esquerda?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_PORTADIANTEIRAESQUERDA
        update.message.reply_text(
            'Como está a porta traseira direita?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_PORTATRASEIRADIREITA

    def lataria_portatraseiradireita(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portatraseiradireita',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portatraseiradireita',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a porta traseira direita?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_PORTATRASEIRADIREITA
        update.message.reply_text(
            'Como está a porta traseira esquerda?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_PORTATRASEIRAESQUERDA

    def lataria_portatraseiraesquerda(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portatraseiraesquerda',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portatraseiraesquerda',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a porta traseira esquerda?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_PORTATRASEIRAESQUERDA
        update.message.reply_text(
            'Como está o porta malas?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_PORTAMALAS

    def lataria_portamalas(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portamalas',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_portamalas',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o porta malas?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_PORTAMALAS
        update.message.reply_text(
            'Como está o parachoque dianteiro?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_PARACHOQUEDIANTEIRO

    def lataria_parachoquedianteiro(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_parachoquedianteiro',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_parachoquedianteiro',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o parachoque dianteiro?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_PARACHOQUEDIANTEIRO
        update.message.reply_text(
            'Como está o parachoque traseiro?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_PARACHOQUETRASEIRO

    def lataria_parachoquetraseiro(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_parachoquetraseiro',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_parachoquetraseiro',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o parachoque traseiro?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_PARACHOQUETRASEIRO
        update.message.reply_text(
            'Como está a lataria do capo?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_CAPO

    def lataria_capo(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_capo',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_capo',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a lataria do capo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_CAPO
        update.message.reply_text(
            'Como está a lataria do teto?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return LATARIA_TETO

    def lataria_teto(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_teto',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'lataria_teto',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a lataria do teto?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return LATARIA_TETO

        reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        update.message.reply_text(
            item.dadosLataria(), parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        return LATARIA_CONFIRM

    def lataria_confirm(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a revisão da parte elétrica do veículo!')

            update.message.reply_text(
                'Como está o farolete?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_FAROLETE
        elif(update.message.text == 'Não, refazer'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos novamente a revisão da lataria do veículo!')

            update.message.reply_text(
                'Como está a lataria dianteira?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return LATARIA_DIANTEIRO
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Opção invalida. Por favor, responda apenas: [Sim, confirmar], [Não, refazer] ou [Cancelar]')
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            update.message.reply_text(
                item.dadosLataria(), parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(
                'O dados informados estão corretos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

    def eletrica_farolete(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_farolete',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_farolete',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o farolete?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_FAROLETE
        update.message.reply_text(
            'Como está o farol baixo?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_FAROLBAIXO

    def eletrica_farolbaixo(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_farolbaixo',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_farolbaixo',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o farol baixo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_FAROLBAIXO
        update.message.reply_text(
            'Como está o farol alto?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_FAROLALTO

    def eletrica_farolalto(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_farolalto',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_farolalto',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o farol alto?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_FAROLALTO
        update.message.reply_text(
            'Como está as setas?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_SETAS

    def eletrica_setas(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_setas',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_setas',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está as setas?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_SETAS
        update.message.reply_text(
            'Como está as luzes do painel?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_LUZESDOPAINEL

    def eletrica_luzesdopainel(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_luzesdopainel',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_luzesdopainel',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está as luzes do painel?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_LUZESDOPAINEL
        update.message.reply_text(
            'Como está as luzes internas?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_LUZESINTERNAS

    def eletrica_luzesinternas(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_luzesinternas',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_luzesinternas',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está as luzes internas?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_LUZESINTERNAS
        update.message.reply_text(
            'Como está a bateria?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_BATERIA

    def eletrica_bateria(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_bateria',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_bateria',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a bateria?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_BATERIA
        update.message.reply_text(
            'Como está o radio?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_RADIO

    def eletrica_radio(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_radio',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_radio',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o radio?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_RADIO
        update.message.reply_text(
            'Como está os autofalantes?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_ALTOFALANTES

    def eletrica_altofalantes(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_altofalantes',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_altofalantes',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está os autofalantes?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_ALTOFALANTES
        update.message.reply_text(
            'Como está o limpador de parabrisa?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_LIMPADORPARABRISA

    def eletrica_limpadorparabrisa(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_limpadorparabrisa',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_limpadorparabrisa',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o limpador de parabrisa?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_LIMPADORPARABRISA
        update.message.reply_text(
            'Como está o ar condicionado?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_ARCONDICIONADO

    def eletrica_arcondicionado(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_arcondicionado',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_arcondicionado',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o ar condicionado?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_ARCONDICIONADO
        update.message.reply_text(
            'Como está as travas?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_TRAVAS

    def eletrica_travas(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_travas',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_travas',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está as travas?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_TRAVAS
        update.message.reply_text(
            'Como está a parte elétrica dos vidros?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return ELETRICA_VIDROS

    def eletrica_vidros(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_vidros',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'eletrica_vidros',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a parte elétrica dos vidros?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return ELETRICA_VIDROS

        reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        update.message.reply_text(
            item.dadosEletrica(), parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        return ELETRICA_CONFIRM

    def eletrica_confirm(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a revisão dos vidros do veículo!')

            update.message.reply_text(
                'Como está o parabrisa?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VIDROS_PARABRISA
        elif(update.message.text == 'Não, refazer'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos novamente a revisão da eletrica do veículo!')

            update.message.reply_text(
                'Como está o farolete',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return ELETRICA_FAROLETE
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Opção invalida. Por favor, responda apenas: [Sim, confirmar], [Não, refazer] ou [Cancelar]')
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            update.message.reply_text(
                item.dadosEletrica(), parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(
                'O dados informados estão corretos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

    def vidros_parabrisa(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'vidros_parabrisa',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'vidros_parabrisa',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o parabrisa?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VIDROS_PARABRISA
        update.message.reply_text(
            'Como está os vidros da lateral esquerda?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return VIDROS_LATERAISESQUERDO

    def vidros_lateraisesquerdo(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'vidros_lateraisesquerdo',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'vidros_lateraisesquerdo',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está os vidros da lateral esquerda?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VIDROS_LATERAISESQUERDO
        update.message.reply_text(
            'Como está os vidros da lateral direita?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return VIDROS_LATERAISDIREITO

    def vidros_lateraisdireito(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'vidros_lateraisdireito',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'vidros_lateraisdireito',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está os vidros da lateral direita?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VIDROS_LATERAISDIREITO
        update.message.reply_text(
            'Como está os vidros traseiros?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return VIDROS_TRASEIRO

    def vidros_traseiro(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'vidros_traseiro',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'vidros_traseiro',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está os vidros traseiros?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return VIDROS_TRASEIRO

        reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        update.message.reply_text(
            item.dadosVidros(), parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        return VIDROS_CONFIRM

    def vidros_confirm(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a revisão dos itens de segurança do veículo!')

            update.message.reply_text(
                'Como está o triangulo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_TRIANGULO
        elif(update.message.text == 'Não, refazer'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos novamente a revisão dos vidros do veículo!')

            update.message.reply_text(
                'Como estão os vidros do parabrisa?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return VIDROS_PARABRISA
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Opção invalida. Por favor, responda apenas: [Sim, confirmar], [Não, refazer] ou [Cancelar]')
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            update.message.reply_text(
                item.dadosSeguranca(), parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(
                'O dados informados estão corretos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

    def seguranca_triangulo(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_triangulo',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_triangulo',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o triangulo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_TRIANGULO
        update.message.reply_text(
            'Como está o extintor?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SEGURANCA_EXTINTOR

    def seguranca_extintor(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_extintor',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_extintor',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o extintor?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_EXTINTOR
        update.message.reply_text(
            'Como está os cintos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SEGURANCA_CINTOS

    def seguranca_cintos(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_cintos',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_cintos',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está os cintos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_CINTOS
        update.message.reply_text(
            'Como está o alarme?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SEGURANCA_ALARME

    def seguranca_alarme(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_alarme',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_alarme',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o alarme?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_ALARME
        update.message.reply_text(
            'Como está as fechaduras?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SEGURANCA_FECHADURAS

    def seguranca_fechaduras(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_fechaduras',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_fechaduras',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está as fechaduras?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_FECHADURAS
        update.message.reply_text(
            'Como está as maçanetas?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SEGURANCA_MACANETAS

    def seguranca_macanetas(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_macanetas',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_macanetas',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está as maçanetas?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_MACANETAS
        update.message.reply_text(
            'Como está os retrovisores?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SEGURANCA_RETROVISORES

    def seguranca_retrovisores(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_retrovisores',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_retrovisores',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está os retrovisores?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_RETROVISORES
        update.message.reply_text(
            'Como está o macaco?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return SEGURANCA_MACACO

    def seguranca_macaco(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_macaco',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'seguranca_macaco',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o macaco?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return SEGURANCA_MACACO

        reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        update.message.reply_text(
            item.dadosSeguranca(), parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        return SEGURANCA_CONFIRM

    def seguranca_confirm(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a revisão dos pneus do veículo!')

            update.message.reply_text(
                'Como está o pneu dianteiro esquerdo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return PNEUS_DIANTEIROESQUERDO
        elif(update.message.text == 'Não, refazer'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos novamente a revisão dos itens de segurança do veículo!')

            update.message.reply_text(
                'Como está o triangulo',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return SEGURANCA_TRIANGULO
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Opção invalida. Por favor, responda apenas: [Sim, confirmar], [Não, refazer] ou [Cancelar]')
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            update.message.reply_text(
                item.dadosSeguranca(), parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(
                'O dados informados estão corretos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

    def pneus_dianteiroesquerdo(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_dianteiroesquerdo',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_dianteiroesquerdo',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o pneu dianteiro esquerdo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return PNEUS_DIANTEIROESQUERDO
        update.message.reply_text(
            'Como está o pneu dianteiro direito?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return PNEUS_DIANTEIRODIREITO

    def pneus_dianteirodireito(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_dianteirodireito',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_dianteirodireito',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o pneu dianteiro direito?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return PNEUS_DIANTEIRODIREITO
        update.message.reply_text(
            'Como está o pneu traseiro esquerdo?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return PNEUS_TRASEIROESQUERDO

    def pneus_traseiroesquerdo(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_traseiroesquerdo',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_traseiroesquerdo',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o pneu traseiro esquerdo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return PNEUS_TRASEIROESQUERDO
        update.message.reply_text(
            'Como está o pneu traseiro direito?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return PNEUS_TRASEIRODIREITO

    def pneus_traseirodireito(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_traseirodireito',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_traseirodireito',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o pneu traseiro direito?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return PNEUS_TRASEIRODIREITO
        update.message.reply_text(
            'Como está o estepe?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return PNEUS_ESTEPE

    def pneus_estepe(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_estepe',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'pneus_estepe',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está o estepe?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return PNEUS_ESTEPE

        reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        update.message.reply_text(
            item.dadosPneus(), parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        return PNEUS_CONFIRM

    def pneus_confirm(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a revisão da higienização do veículo!')

            update.message.reply_text(
                'Como está o higienização externa?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return HIGIENIZACAO_EXTERNA
        elif(update.message.text == 'Não, refazer'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos novamente a revisão dos pneus do veiculo')

            update.message.reply_text(
                'Como está o pneu dianteiro esquerdo?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return PNEUS_DIANTEIROESQUERDO
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Opção invalida. Por favor, responda apenas: [Sim, confirmar], [Não, refazer] ou [Cancelar]')
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            update.message.reply_text(
                item.dadosHigienizacao(), parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(
                'O dados informados estão corretos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

    def higienizacao_externa(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'higienizacao_externa',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'higienizacao_externa',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a higienização externa?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return HIGIENIZACAO_EXTERNA
        update.message.reply_text(
            'Como está a higienização interna?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return HIGIENIZACAO_INTERNA

    def higienizacao_interna(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        if(update.message.text == 'Ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'higienizacao_interna',
                                      True)
        elif(update.message.text == 'Não está ok'):
            listUtils.searchAndUpdate(buff,
                                      update.message.from_user.username,
                                      update.message.chat.id,
                                      'higienizacao_interna',
                                      False)
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')
            update.message.reply_text(
                'Como está a higienização interna?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return HIGIENIZACAO_INTERNA

        reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)
        update.message.reply_text(
            item.dadosHigienizacao(), parse_mode=ParseMode.MARKDOWN)
        update.message.reply_text(
            'O dados informados estão corretos?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
        return HIGIENIZACAO_CONFIRM

    def higienizacao_confirm(self, update, context):
        reply_keyboard = [['Ok'], ['Não está ok']]
        reply_keyboard2 = [['Sim, registrar'],
                           ['Não, finalizar'], ['Cancelar']]

        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Sim, confirmar'):
            update.message.reply_text(
                'Houve alguma não-conformidade?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

            return CONFORMIDADE

        elif(update.message.text == 'Não, refazer'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos novamente a revisão da higienização do veiculo')

            update.message.reply_text(
                'Como está a higienização externa?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return HIGIENIZACAO_EXTERNA
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Opção invalida. Por favor, responda apenas: [Sim, confirmar], [Não, refazer] ou [Cancelar]')
            reply_keyboard2 = [['Sim, confirmar'],
                               ['Não, refazer'], ['Cancelar']]
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            update.message.reply_text(
                item.dadosHigienizacao(), parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(
                'O dados informados estão corretos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))

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
                    str(item.km_inicial) + ' KM',
                    item.dt_abertura
                )

                checklist.km_final = str(item.km_final) + ' KM'
                checklist.dt_fechamento = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")

                checklist_abertura.dt_fechamento = checklist.dt_fechamento

                checklist.carro_p_casa = item.carro_p_casa
                checklist.viajou_c_carro = item.viajou_c_carro
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
                reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True)
            )

            return F_CONFIRM

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


    def conformidade(self, update, context):
        reply_keyboard = [['Sim, registrar'], ['Não, finalizar'], ['Cancelar']]

        if(update.message.text == 'Sim, registrar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Por favor, envie a foto da não conformidade')
            return F_CONFORMIDADE
        elif(update.message.text == 'Não, finalizar'):
            reply_keyboard2 = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]

            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Agora faremos a verificação geral do checklist!')
            if(item.is_abertura):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosAbertura(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosMecanica(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosLataria(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosEletrica(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosVidros(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosSeguranca(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosPneus(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosHigienizacao(), parse_mode=ParseMode.MARKDOWN)
                update.message.reply_text(
                    'O dados informados estão corretos?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
                return A_CONFIRM
            else:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosAbertura(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosMecanica(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosLataria(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosEletrica(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosVidros(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosSeguranca(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosPneus(), parse_mode=ParseMode.MARKDOWN)
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=item.dadosHigienizacao(), parse_mode=ParseMode.MARKDOWN)
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
                'Houve alguma não-conformidade?',
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
                "Agora envie a foto da não conformidade."
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

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Salvo com sucesso!'
        )

        reply_keyboard = [['Sim, registrar'], ['Não, finalizar'], ['Cancelar']]

        update.message.reply_text(
            'Houve mais alguma não-conformidade?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CONFORMIDADE