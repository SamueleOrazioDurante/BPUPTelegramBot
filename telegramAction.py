import os

def sendVideo(bot,message,file):
    with open(file, 'rb') as video:
        bot.send_video(message.chat.id, video)
    os.remove(file)

def sendImage(bot,message,file):
    with open(file, 'rb') as image:
        bot.send_photo(message.chat.id, image)
    os.remove(file)