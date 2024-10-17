
import telebot # telegram bot manager

# general utilities
import os
import urllib.request

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
CHAT_ID = tokenManager.read_chat_id()

bot = telebot.TeleBot(BOT_TOKEN) # instance bot

# extra config for using local telegram API

LOCAL_API = False # by default is FALSE (TO-DO set local API directly on .env)

#bot.log_out() # to log out from telegram base API (only first time)

#telebot.apihelper.API_URL = 'http://0.0.0.0:6969/bot{0}/{1}'
#telebot.apihelper.FILE_URL = 'http://0.0.0.0:6969'

# STARTING MESSAGE ON TELEGRAM (works only if a specific chat_id is set in the config.py or .env)

if(str(CHAT_ID) != "-1"):
    
    START_MESSAGE = open("tutorial", "r").read() # reads and return entire file
    message = bot.send_message(CHAT_ID,START_MESSAGE)

    logger.toConsole("Start message sended to "+CHAT_ID)

# chat id check

class wrongChatID(Exception): pass # expection used

def chat_id_check(message):
    
    # use of string conversion cuz without it doesnt work (idk why)

    if(str(CHAT_ID) == "-1"): # answer to anyone
        return
    else:
        if(str(CHAT_ID) == str(message.chat.id)): # check if chat_id is the same as the message chat id, if it is then answers
            return
        else:  # error, chat id is different than the one in .env file
            raise wrongChatID # use of exception
            
# file size check

class fileSizeTooBIG(Exception): pass # expection used

def check_file_size(filename):
    if(LOCAL_API):
        return
    else:
        if(os.path.getsize(filename) > 50000000): # limit at 50 MB (result of .getsize is in bytes)
            os.remove(filename)
            raise fileSizeTooBIG

# tiktok downloader

@bot.message_handler(regexp="https://vm.tiktok.com/")
def tiktok_dl(message):

    try:
        chat_id_check(message)

        logger.log(" (Tiktok) Richiesta di download: ",message)
        url = message.text

        filename = "tiktok.mp4"
        try:
            urllib.request.urlretrieve(apiRequest.TiktokAPIRequest(TIKTOK_API_TOKEN,url), filename)
            
            try:
                check_file_size(filename)

                telegramAction.sendVideo(bot,message,filename)
                logger.log(" (Tiktok) Video mandato!",message)

            except fileSizeTooBIG:
                logger.error("fileSizeTooBig",message,True)
                bot.send_message(message.chat.id,"Video supera i 50 mb")
            
        except Exception as e:
            logger.error(str(e),message,True) 

    except wrongChatID:
        logger.error("wrongChatID",message,True)


# tiktok quality manager
    
@bot.message_handler(commands=['set_tiktok_quality', 'help'])

def setTiktokQuality(message):

    try:
        chat_id_check(message)

        logger.command(message)
        bot.delete_message(message.chat.id, message.id) # delete initial command
        markupManager.markup_tiktok_quality(bot,message) # sends choices lists

    except wrongChatID:
        logger.error("wrongChatID",message,True)


@bot.callback_query_handler(func=lambda call: True)

def callback_data(call):

    if call.message:
        apiRequest.TIKTOK_QUALITY = call.data # changes quality based on callback data (choices answer)
        logger.log("Qualità impostata a "+apiRequest.TIKTOK_QUALITY,call.message)
        bot.delete_message(call.message.chat.id, call.message.id) # delete choices lists
    
@bot.message_handler(commands=['get_tiktok_quality', 'help'])

def getTiktokQuality(message):

    try: 

        chat_id_check(message)

        logger.command(message)
        bot.send_message(message.chat.id, "Qualità attuale: "+apiRequest.TIKTOK_QUALITY)

    except wrongChatID:
        logger.error("wrongChatID",message,True)

# twitter downloader

@bot.message_handler(regexp="https://x.com/")
def twitter_ss(message):

    try:

        chat_id_check(message)

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

    except wrongChatID:
        logger.error("wrongChatID",message,True)

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

    try:

        chat_id_check(message)
        
        logger.command(message)
        voice_message = message.reply_to_message # get replied message

        bot.delete_message(message.chat.id, message.id) # delete initial command

        file_id = voice_message.voice.file_id  # file size check. If the file is too big, FFmpeg may not be able to handle it.
        file = bot.get_file(file_id)

        response_message = bot.reply_to(voice_message, 'Trascrizione in corso...')

        logger.toConsole(file.file_path)

        file_size = file.file_size
        if int(file_size) >= 1715000:
            bot.edit_message_text(chat_id=response_message.chat.id, message_id=response_message.message_id, text="Audio troppo lungo!")
            return
            # check if message type is supported (audio for now, video/video-audio after)

        try:
            download_file = bot.download_file(file.file_path)  # download file for processing
            with open('audio.ogg', 'wb') as file:
                file.write(download_file)

            transcripted_text = voiceRecognizer.voice_recognizer("it")    # default language: italian # da mettere dentro .env

            logger.log("Speech to text eseguito! Testo: "+transcripted_text,message)

            bot.edit_message_text(chat_id=response_message.chat.id, message_id=response_message.message_id, text=transcripted_text)
            voiceRecognizer.clear()
        except:
            bot.edit_message_text(chat_id=response_message.chat.id, message_id=response_message.message_id, text="Errore. Trascrizione fallita!")

    except wrongChatID:
        logger.error("wrongChatID",message,True)
        pass

@bot.message_handler(commands=['patchnotes', 'Ottiene le ultime patch notes'])
def get_patchnotes(message):

    try:

        chat_id_check(message)

        logger.command(message)

        f = open("patchnotes", "r") # reads and return entire file
        bot.send_message(message.chat.id, f.read())

    except wrongChatID:
        logger.error("wrongChatID",message,True)
        pass

logger.toConsole("---------------------------------------------------")
logger.toConsole("Bot started!")

bot.polling() # bot start
