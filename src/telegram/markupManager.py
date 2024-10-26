import telebot

class Button:
  def __init__(self, text, callback_data):
    self.text = text
    self.callback_data = callback_data

def markup_tiktok_quality(bot,message):

    play = Button("360p","play")
    wmplay = Button("480p","wmplay")
    hdplay = Button("720p","hdplay")

    buttons = [play,wmplay,hdplay]

    markup = markup_builder(3,buttons)

    bot.send_message(message.chat.id, "Seleziona la tipologia:", reply_markup=markup)
    return markup


def markup_builder(markup_row_width,buttons):
    
    markup = telebot.types.InlineKeyboardMarkup(row_width=markup_row_width)
    for button in buttons:
        markup.add(telebot.types.InlineKeyboardButton(button.text, callback_data=button.callback_data))
    return markup