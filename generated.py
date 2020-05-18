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
   update.message.reply_text(
   'Como está o farolete?',
   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
   return ELETRICA_FAROLETE

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
   update.message.reply_text(
   'Como está o parabrisa?',
   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
   return VIDROS_PARABRISA

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
   update.message.reply_text(
   'Como está o triangulo?',
   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
   return SEGURANCA_TRIANGULO

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
   update.message.reply_text(
   'Como está o pneu dianteiro esquerdo?',
   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
   return PNEUS_DIANTEIROESQUERDO

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
   update.message.reply_text(
   'Como está a higienização externa?',
   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
   return HIGIENIZACAO_EXTERNA

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

