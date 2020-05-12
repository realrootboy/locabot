KM_FINAL = 0
CONFORMIDADE = 1
F_CONFORMIDADE = 2
O_CONFORMIDADE = 3

self.conv_handler_fechamento = ConversationHandler(
    entry_points=[CommandHandler(
        'fechar_checklist', self.fechar_checklist)],

    states={
        KM_FINAL: [MessageHandler(Filters.text, self.km_final)],
        CONFORMIDADE: [MessageHandler(Filters.text, self.conformidade)],
        F_CONFORMIDADE: [MessageHandler(Filters.photo, self.f_conformidade)],
        O_CONFORMIDADE: [MessageHandler(Filters.text, self.o_conformidade)],
    },

    fallbacks=[CommandHandler('cancel', self.cancel)]
)


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
            return KM_INICIAL
        if(float(update.message.text) < float(item.km_inicial[:-3])):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Quilometragem final menor que a inicial (inicial:'+str(item.km_inicial)+'). Por favor, informe novamente!')
            return KM_INICIAL
    except:
        replaced = str(update.message.text).replace(',', '.')
        try:
            if(float(replaced) < 0):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Quilometragem inválida. Por favor, informe novamente!')
                return KM_INICIAL
            if(float(update.message.text) < float(item.km_inicial[:-3])):
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Quilometragem final menor que a inicial (inicial:'+str(item.km_inicial)+'). Por favor, informe novamente!')
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
                              'km_final',
                              replaced)

    self.logger.info('Quilometragem final informada por %s: %s',
                     user.first_name, update.message.text)
    update.message.reply_text(
        'Quilometragem final informada: '+update.message.text+'\n')

    reply_keyboard = [['Sim, registrar'], ['Não, finalizar'], ['Cancelar']]

    update.message.reply_text(
        'Houve alguma não-conformidade?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CONFORMIDADE


def conformidade(self, update, context):
    if(update.message.text == 'Sim, registrar'):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Por favor, envie a foto da não conformidade')
        return F_CONFORMIDADE
    elif(update.message.text == 'Não, finalizar'):
        item = listUtils.searchAndGetItem(buff,
                                          update.message.from_user.username,
                                          update.message.chat.id)

        if(update.message.text == 'Não, finalizar'):
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Salvando dados...')

        try:
            Session = Database.Session
            session = Session()

            checklist = session.query(Checklist).filter_by(
                motorista_id=item.motorista_id).order_by(Checklist.id.desc()).first()

            checklist.km_final = item.km_final
            checklist.dt_fechamento = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")

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
            "Agora envie a foto da bomba antes do abastecimento."
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

    print(aux)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Salvo com sucesso!'
    )

    reply_keyboard = [['Sim, registrar'], ['Não, finalizar'], ['Cancelar']]

    update.message.reply_text(
        'Houve mais alguma não-conformidade?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return CONFORMIDADE
