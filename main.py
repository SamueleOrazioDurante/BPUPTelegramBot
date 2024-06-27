
import telebot # telegram bot manager

# general utilities
import os
import urllib.request
import speech_recognition as sr

# script
import tokenManager
import apiRequest
import logger
import telegramAction
import voiceRecognizer
import markupManager

BOT_TOKEN = tokenManager.read_bot_token()
TIKTOK_API_TOKEN = tokenManager.read_tiktok_token()
TWITTER_API_TOKEN = tokenManager.read_twitter_token()

bot = telebot.TeleBot(BOT_TOKEN) # instance bot

# extra config for using local telegram API

# bot.logout() # to log out from telegram base API (only first time)

#apihelper.API_URL = 'http://0.0.0.0:6969/bot{0}/{1}'
#apihelper.FILE_URL = 'http://0.0.0.0:6969'

# tiktok downloader

@bot.message_handler(regexp="https://vm.tiktok.com/")
def tiktok_dl(message):

    logger.log(" (Tiktok) Richiesta di download: ",message)
    url = message.text

    filename = "tiktok.mp4"
    try:
        urllib.request.urlretrieve(apiRequest.TiktokAPIRequest(TIKTOK_API_TOKEN,url), filename)
        
        telegramAction.sendVideo(bot,message,filename)
        logger.log(" (Tiktok) Video mandato!",message)
        
    except Exception as e:
        logger.error(str(e),message,True) 

# tiktok quality manager
    
@bot.message_handler(commands=['set_tiktok_quality', 'help'])
def setTiktokQuality(message):
    logger.command(message)
    bot.delete_message(message.chat.id, message.id) # delete initial command
    markupManager.markup_tiktok_quality(bot,message) # sends choices lists

@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):
    if call.message:
        apiRequest.TIKTOK_QUALITY = call.data # changes quality based on callback data (choices answer)
        logger.log("Qualità impostata a "+apiRequest.TIKTOK_QUALITY,call.message)
        bot.delete_message(call.message.chat.id, call.message.id) # delete choices lists
    
@bot.message_handler(commands=['get_tiktok_quality', 'help'])
def getTiktokQuality(message):
    logger.command(message)
    bot.send_message(message.chat.id, "Qualità attuale: "+apiRequest.TIKTOK_QUALITY)

# twitter downloader

@bot.message_handler(regexp="https://x.com/")
def twitter_ss(message):
    logger.log(" (Twitter) Richiesta di download: ",message)

    url = message.text
    
    try:

        post = apiRequest.TweetAPIRequest(TWITTER_API_TOKEN,url);
        
        # get description and varius images or videos of a post
        text = post[0];
        images = post[1];
        videos = post[2];

        # solo descrizione
        if (len(images) == 0) & (len(videos) == 0):
            exit
        # solo 1 immagine
        elif(len(images) == 1):
            filename = "image.png"
            urllib.request.urlretrieve(images[0], filename)
            telegramAction.sendImage(bot,message,filename)
        # solo 1 video
        elif(len(videos) == 1):
            filename = "video.mp4"
            urllib.request.urlretrieve(videos[0], filename)
            telegramAction.sendVideo(bot,message,filename)
        # solo immagini
        elif(len(videos)==0):
            getImages(images)
            telegramAction.sendMultipleImages(bot,message,len(images))
        # solo video
        elif(len(images)==0):
            getVideos(videos)
            telegramAction.sendMultipleVideos(bot,message,len(videos))
        # misto tra immagini e video
        else:
            telegramAction.sendMultipleImagesVideos(bot,message,len(images),len(videos))
        
        bot.send_message(message.chat.id, text)
        logger.log(" (Twitter) Download eseguito: ",message)
        
    except Exception as e:
        logger.error(str(e),message,True)

def getImages(images):
    i = 0 
    for image in images:
        filename = "image"+str(i)+".jpg"
        urllib.request.urlretrieve(image, filename)
        logger.toConsole("Download effettuato: "+filename)
        i+=1

def getVideos(videos):
    i = 0 
    for video in videos:
        filename = "video"+str(i)+".mp4"
        urllib.request.urlretrieve(video, filename)
        logger.toConsole("Download effettuato: "+filename)
        i+=1

# speech to text

@bot.message_handler(commands=['totext', 'totext'])
def voice_handler(message):
    
    logger.command(message)
    voice_message = message.reply_to_message # get replied message

    bot.delete_message(message.chat.id, message.id) # delete initial command

    file_id = voice_message.voice.file_id  # file size check. If the file is too big, FFmpeg may not be able to handle it.
    file = bot.get_file(file_id)

    logger.toConsole(file.file_path)

    file_size = file.file_size
    if int(file_size) >= 1715000:
        bot.send_message(message.chat.id, 'Upload file size is too large.')
    else:
        download_file = bot.download_file(file.file_path)  # download file for processing
        with open('audio.ogg', 'wb') as file:
            file.write(download_file)

    text = voiceRecognizer.voice_recognizer(sr,'it_IT')    # default language: italian

    logger.log("Speech to text eseguito!",message)
    bot.reply_to(voice_message, text)
    voiceRecognizer.clear()

@bot.message_handler(commands=['patchnotes', 'Ottiene le ultime patch notes'])
def get_patchnotes(message):

    logger.command(message)

    f = open("patchnotes", "r") # reads and return entire file
    bot.send_message(message.chat.id, f.read())

logger.toConsole("---------------------------------------------------")
logger.toConsole("Bot started!")

bot.polling() # bot start
