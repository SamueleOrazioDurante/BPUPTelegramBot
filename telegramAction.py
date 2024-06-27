import telebot
import os
import glob

def sendVideo(bot,message,file):
    with open(file, 'rb') as video:
        bot.send_video(message.chat.id, video)
    os.remove(file)

def sendImage(bot,message,file):
    with open(file, 'rb') as image:
        bot.send_photo(message.chat.id, image)
    os.remove(file)

def sendMultipleImages(bot,message,image_len):
    mediaGroup = [];
    files = [];

    i=0
    while image_len > i:
        filename = "image"+str(i)+".jpg"
        file = open(filename, 'rb');
        files.append(file)
        mediaGroup.append(telebot.types.InputMediaPhoto(file))
        i+=1

    sendMultipleSource(bot,message,mediaGroup,files)

def sendMultipleVideos(bot,message,video_len):
    mediaGroup = [];
    files = [];

    i=0
    while video_len > i:
        filename = "video"+str(i)+".mp4"
        file = open(filename, 'rb');
        files.append(file)
        mediaGroup.append(telebot.types.InputMediaPhoto(file))
        i+=1

    sendMultipleSource(bot,message,mediaGroup,files)

def sendMultipleImagesVideos(bot,message,image_len,video_len):
    mediaGroup = [];
    files = [];

    i=0
    while image_len > i:
        filename = "image"+str(i)+".jpg"
        file = open(filename, 'rb');
        files.append(file)
        mediaGroup.append(telebot.types.InputMediaPhoto(file))
        i+=1

    i=0
    while video_len > i:
        filename = "video"+str(i)+".mp4"
        file = open(filename, 'rb');
        files.append(file)
        mediaGroup.append(telebot.types.InputMediaPhoto(file))
        i+=1

    sendMultipleSource(bot,message,mediaGroup,files)

def sendMultipleSource(bot,message,mediaGroup,files):

    bot.send_media_group(message.chat.id, mediaGroup)


    # garbage cleaner
    
    for file in files:
        file.close()
    
    for jpgpath in glob.iglob(os.path.join(r"./", '*.jpg')):
        os.remove(jpgpath)
    
    for mp4path in glob.iglob(os.path.join(r"./", '*.mp4')):
        os.remove(mp4path)