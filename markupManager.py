import telebot

def markup_tiktok_quality(bot,message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    play = telebot.types.InlineKeyboardButton("360p", callback_data="play")
    wmplay = telebot.types.InlineKeyboardButton("480p", callback_data="wmplay")
    hdplay = telebot.types.InlineKeyboardButton("720p", callback_data="hdplay")
    markup.add(play, wmplay,hdplay)
    bot.send_message(message.chat.id, "Seleziona la tipologia:", reply_markup=markup)
    return markup