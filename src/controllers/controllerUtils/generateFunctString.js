const a = (to_obj, self_s, self_f, next_s, next_f) => {
  return `def ${to_obj}(self, update, context):\n` +
    "   reply_keyboard = [['Ok'], ['Não está ok']]\n" +
    "   if(update.message.text == 'Ok'):\n" +
    "      listUtils.searchAndUpdate(buff,\n" +
    "        update.message.from_user.username,\n" +
    "        update.message.chat.id,\n" +
    `        '${to_obj}',\n` +
    "        True)\n" +
    "   elif(update.message.text == 'Não está ok'):\n" +
    "      listUtils.searchAndUpdate(buff,\n" +
    "        update.message.from_user.username,\n" +
    "        update.message.chat.id,\n" +
    `        '${to_obj}',\n` +
    "        False)\n" +
    "   else:\n" +
    "      context.bot.send_message(\n" +
    "        chat_id=update.effective_chat.id,\n" +
    "        text='Resposta inválida, por favor, responda apenas [Ok] ou [Não está ok]')\n" +
    "      update.message.reply_text(\n" +
    `        'Como está ${self_s}?',\n` +
    "      reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))\n" +
    `      return ${self_f}\n` +
    "   update.message.reply_text(\n" +
    `   'Como está ${next_s}?',\n` +
    "   reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))\n" +
    `   return ${next_f}\n\n`
}

const vars = [
  { to_obj: 'lataria_dianteiro', self_s: 'a lataria dianteira', },
  { to_obj: 'lataria_traseiro', self_s: 'a lataria traseira', },
  { to_obj: 'lataria_portadianteiradireita', self_s: 'a porta dianteira direita', },
  { to_obj: 'lataria_portadianteiraesquerda', self_s: 'a porta dianteira esquerda', },
  { to_obj: 'lataria_portatraseiradireita', self_s: 'a porta traseira direita', },
  { to_obj: 'lataria_portatraseiraesquerda', self_s: 'a porta traseira esquerda', },
  { to_obj: 'lataria_portamalas', self_s: 'o porta malas', },
  { to_obj: 'lataria_parachoquedianteiro', self_s: 'o parachoque dianteiro', },
  { to_obj: 'lataria_parachoquetraseiro', self_s: 'o parachoque traseiro', },
  { to_obj: 'lataria_capo', self_s: 'a lataria do capo', },
  { to_obj: 'lataria_teto', self_s: 'a lataria do teto', },
  { to_obj: 'eletrica_farolete', self_s: 'o farolete', },
  { to_obj: 'eletrica_farolbaixo', self_s: 'o farol baixo', },
  { to_obj: 'eletrica_farolalto', self_s: 'o farol alto', },
  { to_obj: 'eletrica_setas', self_s: 'as setas', },
  { to_obj: 'eletrica_luzesdopainel', self_s: 'as luzes do painel', },
  { to_obj: 'eletrica_luzesinternas', self_s: 'as luzes internas', },
  { to_obj: 'eletrica_bateria', self_s: 'a bateria', },
  { to_obj: 'eletrica_radio', self_s: 'o radio', },
  { to_obj: 'eletrica_altofalantes', self_s: 'os autofalantes', },
  { to_obj: 'eletrica_limpadorparabrisa', self_s: 'o limpador de parabrisa', },
  { to_obj: 'eletrica_arcondicionado', self_s: 'o ar condicionado', },
  { to_obj: 'eletrica_travas', self_s: 'as travas', },
  { to_obj: 'eletrica_vidros', self_s: 'a parte elétrica dos vidros', },
  { to_obj: 'vidros_parabrisa', self_s: 'o parabrisa', },
  { to_obj: 'vidros_lateraisesquerdo', self_s: 'os vidros da lateral esquerda', },
  { to_obj: 'vidros_lateraisdireito', self_s: 'os vidros da lateral direita', },
  { to_obj: 'vidros_traseiro', self_s: 'os vidros traseiros', },
  { to_obj: 'seguranca_triangulo', self_s: 'o triangulo', },
  { to_obj: 'seguranca_extintor', self_s: 'o extintor', },
  { to_obj: 'seguranca_cintos', self_s: 'os cintos', },
  { to_obj: 'seguranca_alarme', self_s: 'o alarme', },
  { to_obj: 'seguranca_fechaduras', self_s: 'as fechaduras', },
  { to_obj: 'seguranca_macanetas', self_s: 'as maçanetas', },
  { to_obj: 'seguranca_retrovisores', self_s: 'os retrovisores', },
  { to_obj: 'seguranca_macaco', self_s: 'o macaco', },
  { to_obj: 'pneus_dianteiroesquerdo', self_s: 'o pneu dianteiro esquerdo', },
  { to_obj: 'pneus_dianteirodireito', self_s: 'o pneu dianteiro direito', },
  { to_obj: 'pneus_traseiroesquerdo', self_s: 'o pneu traseiro esquerdo', },
  { to_obj: 'pneus_traseirodireito', self_s: 'o pneu traseiro direito', },
  { to_obj: 'pneus_estepe', self_s: 'o estepe', },
  { to_obj: 'higienizacao_externa', self_s: 'a higienização externa', },
  { to_obj: 'higienizacao_interna', self_s: 'a higienização interna', }]

const fs = require('fs');

for (let i = 0; i < vars.length - 1 ; i++) {
  fs.appendFileSync('generated.py', 
    a(vars[i].to_obj,
      vars[i].self_s,
      vars[i].to_obj.toUpperCase(),
      vars[i + 1].self_s,
      vars[i + 1].to_obj.toUpperCase()
    ))
}