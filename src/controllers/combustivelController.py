from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, CallbackQueryHandler)

from datetime import datetime
from pytz import timezone

import xlsxwriter
import shutil
import os

from controllers.controllerUtils import listUtils

from models.regAbastecimento import RegAbastecimento
from models.Motorista import Motorista
from models.Registro import Registro
from models.Veiculos import Veiculos

from utils import textLogger
from utils import CalendarUtils
from drive import gdrive

from database.main import Database


RETORNO, PLACA, QUILOMETRAGEM, QNT_LITRO, VAL_LITRO, VAL_TOTAL, TP_COMBUSTIVEL, POSTO, BOMBAINICIO, FPLACA, BOMBAFIM, PAINEL, NFISCAL, CONFIRM = range(
    14)

buff = list()


class CombustivelController:
    def __init__(self, logger):
        self.logger = logger
        self.conv_handler = ConversationHandler(
            entry_points = [CommandHandler('combustivel', self.registro)],

            states = {
                RETORNO: [MessageHandler(Filters.text & (~ Filters.command), self.retorno)],
                PLACA: [MessageHandler(Filters.text & (~ Filters.command), self.placa)],
                QUILOMETRAGEM: [MessageHandler(Filters.text & (~ Filters.command), self.quilometragem)],
                QNT_LITRO: [MessageHandler(Filters.text & (~ Filters.command), self.qnt_litro)],
                VAL_LITRO: [MessageHandler(Filters.text & (~ Filters.command), self.val_litro)],
                TP_COMBUSTIVEL: [MessageHandler(Filters.text & (~ Filters.command), self.tp_combustivel)],
                POSTO: [MessageHandler(Filters.text & (~ Filters.command), self.posto)],
                BOMBAINICIO: [MessageHandler(Filters.photo, self.bombainicio)],
                FPLACA: [MessageHandler(Filters.photo, self.fplaca)],
                BOMBAFIM: [MessageHandler(Filters.photo, self.bombafim)],
                PAINEL: [MessageHandler(Filters.photo, self.painel)],
                NFISCAL: [MessageHandler(Filters.photo, self.nfiscal)],
                CONFIRM: [MessageHandler(Filters.text & (~ Filters.command), self.confirm)]
            },

            fallbacks = [CommandHandler('cancelar', self.cancel)]
        )

    def registro(self, update, context):
        placas = []
        if update.callback_query:
            try:
                current_chat_id = update.callback_query.message.chat.id
                current_username = update.callback_query.from_user.username
                abastecimento = RegAbastecimento(current_username, current_chat_id)
                buff.append(abastecimento)
            except Exception as e:
                context.bot.send_message(
                    chat_id=current_chat_id,
                    text='Não é possível realizar o cadastro de combustível sem um nome de usuário cadastrado.');
                return ConversationHandler.END
        else:
            try:
                current_chat_id = update.message.chat.id
                current_username = update.message.from_user.username
                abastecimento = RegAbastecimento(current_username, current_chat_id)
                buff.append(abastecimento)
            except Exception as e:
                update.message.reply_text(
                    'Não é possível realizar o cadastro de combustível sem um nome de usuário cadastrado.',
                    reply_markup=ReplyKeyboardRemove()
                )
                return ConversationHandler.END
        
        try:
            Session = Database.Session
            session = Session()

            motorista = session.query(Motorista).filter_by(telegram_user=current_username).first()

            if motorista is None:
                context.bot.send_message(
                    chat_id=current_chat_id,
                    text='Usuário ' + current_username + ' não encontrado na base de dados. ' + 
                    'Acesso não autorizado!', reply_markup=ReplyKeyboardRemove()
                )
                session.close()
                buff.remove(abastecimento)
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
            buff.remove(abastecimento)
            return ConversationHandler.END

        context.bot.send_message(
            chat_id=current_chat_id,
            text='Olá, ' + motorista.nome + '. Por favor, informe a placa do veículo.',
            reply_markup=ReplyKeyboardMarkup(placas, one_time_keyboard=True))
        
        return PLACA

    def retorno(self, update, context):
        placas = []
        try:
            abastecimento = RegAbastecimento(
                update.message.from_user.username, update.message.chat.id)
            buff.append(abastecimento)
        except:
            update.message.reply_text(
                'Não é possível realizar o cadastro de combustível sem um nome de usuário cadastrado.',
                reply_markup=ReplyKeyboardRemove()
            )
            return ConversationHandler.END
        
        try:
            Session = Database.Session
            session = Session()

            motorista = session.query(Motorista).filter_by(telegram_user=update.message.from_user.username).first()

            if motorista is None:
                update.message.reply_text(
                    'Usuário ' + update.message.from_user.username + ' não encontrado na base de dados. ' + 
                    'Acesso não autorizado!', reply_markup=ReplyKeyboardRemove()
                )
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

        if(float(update.message.text.replace(',', '.')) > 200):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='A quantidade do litros abastecidos inserida é muito grande (limite de 200L). Por favor, informe novamente o valor correto!\n Lembre-se de enviar o valor com vírgula ou ponto, ex: 3,65 no lugar de 365')
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

        if(float(update.message.text.replace(',', '.')) > 10):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='O valor do litro inserido é muito grande (limite de R$ 10,00). Por favor, informe novamente!\n Lembre-se de enviar o valor com vírgula ou ponto, ex: 3,65 no lugar de 365')
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

        reply_keyboard = [['DIESEL COMUM', 'DIESEL S-10'],
                          ['GASOLINA ADITIVIDADA', 'GASOLINA COMUM']]

        if not update.message.text in ['DIESEL COMUM', 'DIESEL S-10', 'GASOLINA ADITIVIDADA', 'GASOLINA COMUM']:
            update.message.reply_text('Combustível inválido, por favor informe o tipo correto de combustivel.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            
            return TP_COMBUSTIVEL

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
                          ['TIMBOZAO / TREMENDAO', 'RAIZ'],
                          ['TANGUA', 'TREVÃO'],
                          ['CAJU', 'TICKTLOG'],
                          ['NOSSA SENHORA DE FATIMA', 'SÃO CRISTOVÃO'],
                          ['GUARAVE', 'GUARAVE FILIAL'],
                          ['CARAVELA'],
                          ['SANTA AMÉLIA', 'TULIPA'],
                          ['GOODCARD', 'REEMBOLSO']]

        update.message.reply_text(
            'Combustível informado: '+update.message.text+'\n'
            'Agora informe o posto:',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return POSTO

    def posto(self, update, context):
        user = update.message.from_user

        reply_keyboard = [['MARLIN', 'LIDER'],
                          ['OURO NEGRO', 'RIO NEGRO'],
                          ['DAMIANI', 'JR / DALLAS'],
                          ['TIMBOZAO / TREMENDAO', 'RAIZ'],
                          ['TANGUA', 'TREVÃO'],
                          ['CAJU', 'TICKTLOG'],
                          ['NOSSA SENHORA DE FATIMA', 'SÃO CRISTOVÃO'],
                          ['GUARAVE', 'GUARAVE FILIAL'],
                          ['CARAVELA'],
                          ['SANTA AMÉLIA', 'TULIPA'],
                          ['GOODCARD', 'REEMBOLSO']]

        if not update.message.text in ['MARLIN', 'LIDER',
                          'OURO NEGRO', 'RIO NEGRO',
                          'DAMIANI', 'JR / DALLAS',
                          'TIMBOZAO / TREMENDAO', 'RAIZ', 'CAJU', 'TICKTLOG',
                          'NOSSA SENHORA DE FATIMA', 'SÃO CRISTOVÃO',
                          'GUARAVE', 'GUARAVE FILIAL', 'CARAVELA',
                          'SANTA AMÉLIA', 'TULIPA',
                          'GOODCARD', 'REEMBOLSO', 'TANGUA', 'TREVÃO']:
            update.message.reply_text('Posto inválido, por favor informe o posto correto.',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            
            return POSTO

        listUtils.searchAndUpdate(buff,
                                  update.message.from_user.username,
                                  update.message.chat.id,
                                  'posto',
                                  update.message.text)

        self.logger.info('Posto informado por %s: %s',
                         user.first_name, update.message.text)

        update.message.reply_text(
            "Agora envie a foto da bomba antes do abastecimento."
        )

        return BOMBAINICIO

    def bombainicio(self, update, context):
        try:
            file_id = update.message.photo[-1].file_id
            newFile = context.bot.getFile(file_id)
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            os.mkdir('media/'+item.media_dir)
            newFile.download('media/' + item.media_dir + '/bomba_antes.jpg')
        except:
            update.message.reply_text(
                "Ocorreu um erro! Tente enviar apenas uma foto de uma vez. " +
                "Agora envie a foto da bomba antes do abastecimento."
            )
            listUtils.listItens(buff)
            return BOMBAINICIO

        update.message.reply_text(
            "Agora envie a foto da placa do veículo."
        )

        return FPLACA

    def fplaca(self, update, context):
        try:
            file_id = update.message.photo[-1].file_id
            newFile = context.bot.getFile(file_id)
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            newFile.download('media/' + item.media_dir + '/placa.jpg')
        except:
            update.message.reply_text(
                "Ocorreu um erro! Tente enviar apenas uma foto de uma vez. " +
                "Agora envie a foto da placa do veículo."
            )
            return FPLACA

        update.message.reply_text(
            "Agora envie a foto da bomba após o abastecimento."
        )

        return BOMBAFIM

    def bombafim(self, update, context):
        try:
            file_id = update.message.photo[-1].file_id
            newFile = context.bot.getFile(file_id)
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            newFile.download('media/' + item.media_dir + '/bomba_depois.jpg')
        except:
            update.message.reply_text(
                "Ocorreu um erro! Tente enviar apenas uma foto de uma vez. " +
                "Agora envie a foto da bomba após o abastecimento."
            )
            return

        update.message.reply_text(
            "Agora envie a foto do painel do veículo."
        )

        return PAINEL

    def painel(self, update, context):
        try:
            file_id = update.message.photo[-1].file_id
            newFile = context.bot.getFile(file_id)
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            newFile.download('media/' + item.media_dir + '/painel.jpg')
        except:
            update.message.reply_text(
                "Ocorreu um erro! Tente enviar apenas uma foto de uma vez. " +
                "Agora envie a foto do painel do veículo."
            )
            return PAINEL

        update.message.reply_text(
            "Agora envie a foto da nota fiscal."
        )

        return NFISCAL

    def nfiscal(self, update, context):
        try:
            file_id = update.message.photo[-1].file_id
            newFile = context.bot.getFile(file_id)
            item = listUtils.searchAndGetItem(buff,
                                              update.message.from_user.username,
                                              update.message.chat.id)
            newFile.download('media/' + item.media_dir + '/nota_fiscal.jpg')
        except:
            update.message.reply_text(
                "Ocorreu um erro! Tente enviar apenas uma foto de uma vez." +
                "Agora envie a foto da nota fiscal."
            )
            return NFISCAL

        try:
            a = float(str(item.qnt_litro).replace(',', '.'))
            b = float(str(item.val_litro).replace(',', '.'))
            item.val_total = str(round(float(a*b),2)).replace('.', ',')

            update.message.reply_text(
                item.stringData(), parse_mode=ParseMode.MARKDOWN)

            reply_keyboard = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]

            update.message.reply_text(
                'O dados informados estão corretos?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return CONFIRM
        except Exception as e:
            try:
                    context.bot.send_message(
                        chat_id=445181781,
                        text=str(e))
            except:
                print('err in send')
                update.message.reply_text('Houve um erro ao tentar salvar! ' +
                                          'O erro foi reportado, tente novamente mais tarde.',
                                          reply_markup=ReplyKeyboardRemove())
            textLogger.log('Combustivel - ' + str(e))
            print(e)
            buff.pop(buff.index(item))
            return ConversationHandler.END
        
    def confirm(self, update, context):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if not item:
            update.message.reply_text('Houve um erro ao tentar salvar! ' +
                                          'O erro foi reportado, tente novamente mais tarde.',
                                          reply_markup=ReplyKeyboardRemove())
            buff.clear()
            textLogger.log('Combustivel - not item ;' + listUtils.listItens(buff))

        if(update.message.text == 'Sim, confirmar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...')

            try:
                Session = Database.Session
                session = Session()

                motorista = session.query(Motorista).filter_by(telegram_user=item.username).first()

                registro = Registro(
                    motorista,
                    item.placa,
                    str(item.quilometragem) + ' KM',
                    str(item.qnt_litro) + ' L',
                    'R$ ' + str(item.val_litro),
                    'R$ ' + str(item.val_total),
                    item.tp_combustivel,
                    item.posto,
                    item.media_dir
                )

                session.add(registro)
                session.commit()

                session.close()
            except Exception as e:
                try:
                    context.bot.send_message(
                        chat_id=445181781,
                        text=str(e))
                except:
                    print('err in send')
                update.message.reply_text('Houve um erro ao tentar salvar! ' +
                                          'O erro foi reportado, tente novamente mais tarde.',
                                          reply_markup=ReplyKeyboardRemove())
                textLogger.log('Combustivel - ' + str(e))
                print(e)
                buff.pop(buff.index(item))
                return ConversationHandler.END

            buff.pop(buff.index(item))

            update.message.reply_text('Dados enviados com sucesso! Caso haja alguma inconsistência favor informar para @renanmgomes ou @igorpittol.',
                                      reply_markup=ReplyKeyboardRemove())

            local_path = 'media/ABASTECIMENTO-' + datetime.now(timezone('America/Sao_Paulo')).strftime('%b-%Y') + '.xlsx'
            register_now = datetime.now(timezone('America/Sao_Paulo'))

            range_intervalo = CalendarUtils.getRangeByMonth(register_now.month, register_now.year)
            
            Session = Database.Session
            session = Session()

            registros = session.query(Registro).filter(
                Registro.created_at >= range_intervalo[0],
                Registro.created_at < range_intervalo[1]
            )
            try:
                workbook = xlsxwriter.Workbook(local_path)
                worksheet = workbook.add_worksheet()

                row = 0
                col = 0

                for registro in registros:
                    worksheet.write(row, col + 0, registro.id)
                    worksheet.write(row, col + 1, str(registro.created_at.astimezone(timezone('America/Sao_Paulo')).day) + '/' 
                    + str(registro.created_at.astimezone(timezone('America/Sao_Paulo')).month)
                    + '/' + str(registro.created_at.astimezone(timezone('America/Sao_Paulo')).year))
                    worksheet.write(row, col + 2, registro.created_at.astimezone(timezone('America/Sao_Paulo')).strftime('%H:%M'))
                    worksheet.write(row, col + 3, registro.posto)
                    worksheet.write(row, col + 4, ' ')
                    worksheet.write(row, col + 5, CalendarUtils.REV_FULL_MONTHS[registro.created_at.month])
                    worksheet.write(row, col + 6, registro.placa)
                    worksheet.write(row, col + 7, registro.quilometragem.replace(' KM', ''))
                    worksheet.write(row, col + 8, registro.created_at.year)
                    worksheet.write(row, col + 9, registro.qnt_litro.replace(' L', ''))
                    worksheet.write(row, col + 10, registro.val_litro.replace('R$ ', ''))
                    worksheet.write(row, col + 11, registro.motorista.nome)
                    worksheet.write(row, col + 12, registro.tp_combustivel.split(' ')[0])
                    worksheet.write(row, col + 13, registro.tp_combustivel)
                    worksheet.write(row, col + 14, registro.val_total.replace('R$ ', ''))
                    row += 1
                
                workbook.close()

            except Exception as e:

                print(e)
                session.close()
                gdrive.upload_gdrive(local_path, local_path.replace('media/', ''))
                os.remove(local_path)
                return ConversationHandler.END

            session.close()
            gdrive.upload_gdrive(local_path, local_path.replace('media/', ''))
            os.remove(local_path)
            return ConversationHandler.END

        elif(update.message.text == 'Não, refazer'):
            update.message.reply_text(
                'Ok! Vamos refazer então.',
                reply_markup=ReplyKeyboardMarkup([['Continuar']], one_time_keyboard=True))

            shutil.rmtree('media/' + item.media_dir , ignore_errors=True)

            buff.pop(buff.index(item))

            return RETORNO
        elif(update.message.text == 'Cancelar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Operação cancelada!')

            shutil.rmtree('media/' + item.media_dir , ignore_errors=True)

            buff.pop(buff.index(item))

            return ConversationHandler.END
        else:
            reply_keyboard = [['Sim, confirmar'], ['Não, refazer'], ['Cancelar']]
                        
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Resposta inválida, por favor, responda apenas [Sim, confirmar], [Não, refazer] ou [Cancelar]')
            update.message.reply_text(
                item.stringData(), parse_mode=ParseMode.MARKDOWN)
            update.message.reply_text(
                    'O dados informados estão corretos?',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

            return CONFIRM

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
