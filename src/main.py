import telebot # telegram bot manager

from groq import Groq # IA LLM

# general utilities
import os
import urllib.request
from threading import Thread,Event
from time import sleep
import traceback

# script
import auth.tokenManager as tokenManager
import utilities.apiRequest as apiRequest
import logger.logger as logger
import telegram.telegramAction as telegramAction
if(tokenManager.read_stt_type() == "WHISPER"):
    import utilities.whisper as voiceRecognizer
elif(tokenManager.read_stt_type() == "VOSK"):
    import utilities.vosk as voiceRecognizer
else:
    import utilities.whisperx as voiceRecognizer
import telegram.markupManager as markupManager
import utilities.textToSpeech as textToSpeech
import utilities.fileManager as fileManager
import utilities.statsManager as stats

BOT_TOKEN = tokenManager.read_bot_token()
CHAT_ID = tokenManager.read_chat_id()

def send_long_message(bot, chat_id, text, disable_notification=True, reply_to_message_id=None):
    max_len = 4096
    for i in range(0, len(text), max_len):
        chunk = text[i:i + max_len]
        bot.send_message(chat_id, chunk, disable_notification=disable_notification, reply_to_message_id=reply_to_message_id)

def clean_think_tags(text):
    import re
    # Remove <think> ... </think> blocks
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return text.strip()

bot = telebot.TeleBot(BOT_TOKEN) # instance bot

# extra config for using local telegram API

LOCAL_API = False # by default is FALSE (TO-DO set local API directly on .env)

#bot.log_out() # to log out from telegram base API (only first time)

#telebot.apihelper.API_URL = 'http://0.0.0.0:6969/bot{0}/{1}'
#telebot.apihelper.FILE_URL = 'http://0.0.0.0:6969'

# STARTING MESSAGE ON TELEGRAM (works only if a specific chat_id is set in the config.py or .env)

if(str(CHAT_ID) != "-1"):
    if(tokenManager.read_welcome_message() == True):
        START_MESSAGE = open("data/tutorial", "r").read() # reads and return entire file
        send_long_message(bot, CHAT_ID, START_MESSAGE, disable_notification=True)

        logger.toConsole("Start message sended to "+CHAT_ID)

# IA Client Init
if tokenManager.read_groq_api_key() == None:
    client = None
    logger.toConsole("IA LLM Groq client not initialized. GROQ_API_KEY not provided.")
else:
    client = Groq(
        api_key=tokenManager.read_groq_api_key()
    )
    logger.toConsole("IA LLM Groq client initialized.")

# useless file clear

logger.toConsole("Useless file cleaning...")
exts = ["mp3","mp4","wav"]
fileManager.clean_extensions(exts)
logger.toConsole("File cleared!")

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

        logger.telegramMessage(" (Tiktok) Richiesta di download: ",message)
        stats.addAPIRequest("tiktok",str(message.from_user.username))
        url = message.text

        filename = "tiktok.mp4"
        try:
            link = apiRequest.TiktokAPIRequest(url)

            if not link == None:
                urllib.request.urlretrieve(link, filename)
                
                try:
                    check_file_size(filename)

                    telegramAction.sendVideo(bot,message,filename)
                    logger.telegramMessage(" (Tiktok) Video mandato!",message)

                except fileSizeTooBIG:
                    logger.telegramError("fileSizeTooBig",message)
                    bot.send_message(message.chat.id,"Video supera i 50 mb",disable_notification=True)
            else:
                logger.apiRequest(link,"Tiktok API Key non impostata") 
                bot.send_message(message.chat.id,"Tiktok API Key non impostata",disable_notification=True)
        except Exception as e:
            logger.telegramError(str(traceback.format_exc()),message) 

    except wrongChatID:
        logger.telegramError("wrongChatID",message)


# tiktok quality manager
    
@bot.message_handler(commands=['set_tiktok_quality', 'help'])

def setTiktokQuality(message):

    try:
        chat_id_check(message)

        logger.command(message)
        bot.delete_message(message.chat.id, message.id) # delete initial command
        markupManager.markup_tiktok_quality(bot,message) # sends choices lists

    except wrongChatID:
        logger.telegramError("wrongChatID",message)


@bot.callback_query_handler(func=lambda call: True)

def callback_data(call):

    if call.message:
        apiRequest.TIKTOK_QUALITY = call.data # changes quality based on callback data (choices answer)
        logger.telegramMessage("Qualità impostata a "+apiRequest.TIKTOK_QUALITY,call.message)
        bot.delete_message(call.message.chat.id, call.message.id) # delete choices lists
    
@bot.message_handler(commands=['get_tiktok_quality', 'help'])

def getTiktokQuality(message):

    try: 

        chat_id_check(message)

        logger.command(message)
        bot.send_message(message.chat.id, "Qualità attuale: "+apiRequest.TIKTOK_QUALITY,disable_notification=True)

    except wrongChatID:
        logger.telegramError("wrongChatID",message)

# twitter downloader

@bot.message_handler(regexp="https://x.com/")
def twitter_ss(message):    

    try:

        chat_id_check(message)

        stats.addAPIRequest("twitter",str(message.from_user.username))
        logger.telegramMessage(" (Twitter) Richiesta di download: ",message)
        

        try:
            
            url = message.text
            post = apiRequest.TweetAPIRequest(url)
            
            if not post == None:
                
                # get description and varius images or videos of a post
                text = post[0]
                images = post[1]
                videos = post[2]

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
                
                send_long_message(bot, message.chat.id, text, disable_notification=True)
                logger.telegramMessage(" (Twitter) Download eseguito: ",message)
            
            else:
                logger.apiRequest(post,"Twitter API Key non impostata") 
                bot.send_message(message.chat.id,"Twitter API Key non impostata",disable_notification=True)
        
        except Exception as e:
            bot.send_message(message.chat.id, "Nessun media trovato",disable_notification=True)
            logger.telegramError(str(traceback.format_exc()),message)

    except wrongChatID:
        logger.telegramError("wrongChatID",message)

def getImages(images):
    i = 0 
    for image in images:
        logger.toConsole("Tentativo di dl (image): "+image)
        filename = "image"+str(i)+".jpg"

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (U; Linux i583 x86_64; en-US) Gecko/20100101 Firefox/63.0')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(image, filename)
        logger.toConsole("Download effettuato: "+filename)
        i+=1

def getVideos(videos):
    i = 0 
    for video in videos:
        logger.toConsole("Tentativo di dl (video): "+video)
        filename = "video"+str(i)+".mp4"

        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (U; Linux i583 x86_64; en-US) Gecko/20100101 Firefox/63.0')]
        urllib.request.install_opener(opener)

        urllib.request.urlretrieve(video, filename)
        logger.toConsole("Download effettuato: "+filename)
        i+=1

# instagram downloader
@bot.message_handler(regexp="https://www.instagram.com/p/")
def instagram_p_ss(message):
    instagram_ss(message)

@bot.message_handler(regexp="https://www.instagram.com/reel/")

def instagram_ss(message):

    try:

        chat_id_check(message)

        stats.addAPIRequest("instagram",str(message.from_user.username))
        logger.telegramMessage(" (Instagram) Richiesta di download: ",message)

        url = message.text
        
        try:
            if url[26:][:1] == "p":
                reel_id = url[28:][:11]
            else:
                reel_id = url[31:][:11]

            post = apiRequest.InstaAPIRequest(reel_id);
            
            if not post == None:

                # get description and varius images or videos of a post
                text = post[0]
                images = post[1]
                videos = post[2]

                # solo descrizione
                if (len(images) == 0) & (len(videos) == 0):
                    pass
                # solo 1 immagine
                elif(len(images) == 1):
                    filename = "image.png"
                    logger.toConsole("Tentativo di dl (image): "+images[0])

                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (U; Linux i583 x86_64; en-US) Gecko/20100101 Firefox/63.0')]
                    urllib.request.install_opener(opener)

                    urllib.request.urlretrieve(images[0], filename)
                    telegramAction.sendImage(bot,message,filename)
                # solo 1 video
                elif(len(videos) == 1):
                    filename = "video.mp4"
                    logger.toConsole("Tentativo di dl (video): "+videos[0])

                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (U; Linux i583 x86_64; en-US) Gecko/20100101 Firefox/63.0')]
                    urllib.request.install_opener(opener)

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
                    getImages(images)
                    getVideos(videos)
                    telegramAction.sendMultipleImagesVideos(bot,message,len(images),len(videos))
                
                if text != "": # send caption only if there is one
                    send_long_message(bot, message.chat.id, text, disable_notification=True)

                logger.telegramMessage(" (Instagram) Download eseguito: ",message)
            
            else:
                logger.apiRequest(post,"Instagram API Key non impostata") 
                bot.send_message(message.chat.id,"Instagram API Key non impostata",disable_notification=True)

        except Exception as e:
           bot.send_message(message.chat.id, "Nessun media trovato",disable_notification=True)
           logger.telegramError(str(traceback.format_exc()),message)


    except wrongChatID:
        logger.telegramError("wrongChatID",message)


# speech to text

@bot.message_handler(commands=['totext', 'totext'])
def voice_handler(message):
    try:
        chat_id_check(message)
        
        stats.addCommand("totext", str(message.from_user.username))
        logger.command(message)

        file_message = message.reply_to_message
        bot.delete_message(message.chat.id, message.id)
        
        # Invia un messaggio per indicare che la richiesta è in coda
        queue_status = voiceRecognizer.get_queue_status()
        position = queue_status["position"] + 1  # +1 per includere questa richiesta
        
        initial_message = f"Richiesta in coda. Posizione: {position}" if position > 0 else "In corso..."
        response_message = bot.reply_to(file_message, initial_message, disable_notification=True)
        
        # Callback che verrà chiamata quando la trascrizione è completata
        def transcription_complete(result):
            bot.edit_message_text(chat_id=response_message.chat.id, 
                                 message_id=response_message.message_id, 
                                 text=result)
            logger.telegramMessage("Speech to text completato! Testo: " + result, message)
        
        try:
            # File audio
            if hasattr(file_message, 'voice') and file_message.voice:
                file_id = file_message.voice.file_id
                file = bot.get_file(file_id)
                download_file = bot.download_file(file.file_path)
                
                ogg_audio_path = f"temp/audio_{message.id}.ogg"
                with open(ogg_audio_path, 'wb') as file:
                    file.write(download_file)
                
                # Aggiunge alla coda invece di elaborare immediatamente
                voiceRecognizer.queue_transcription_request(ogg_audio_path, "audio", transcription_complete)
                
            # File video
            elif hasattr(file_message, 'video') and file_message.video:
                file_id = file_message.video.file_id
                file = bot.get_file(file_id)
                download_file = bot.download_file(file.file_path)
                
                mp4_audio_path = f"temp/video_{message.id}.mp4"
                with open(mp4_audio_path, 'wb') as file:
                    file.write(download_file)
                
                voiceRecognizer.queue_transcription_request(mp4_audio_path, "video", transcription_complete)
                
            # File video_note
            elif hasattr(file_message, 'video_note') and file_message.video_note:
                file_id = file_message.video_note.file_id
                file = bot.get_file(file_id)
                download_file = bot.download_file(file.file_path)
                
                mp4_audio_path = f"temp/video_{message.id}.mp4"
                with open(mp4_audio_path, 'wb') as file:
                    file.write(download_file)
                
                voiceRecognizer.queue_transcription_request(mp4_audio_path, "video", transcription_complete)
                
            else:
                bot.edit_message_text(chat_id=response_message.chat.id, 
                                     message_id=response_message.message_id, 
                                     text="Errore. Formato non supportato!")
                
        except Exception as e:
            logger.toConsole(f"STT errore: {str(e)}")
            bot.edit_message_text(chat_id=response_message.chat.id, 
                                 message_id=response_message.message_id, 
                                 text=f"Errore: {str(e)}")
            
    except wrongChatID:
        logger.telegramError("wrongChatID", message)
        pass

def voice_text_reply_animator(response_message,event):

    text = "In corso.."
    counter = 0
    while True:
        
        if counter == 5:
            text = "In corso."
            counter = 0

        bot.edit_message_text(chat_id=response_message.chat.id, message_id=response_message.message_id, text=text)
        text +="."

        counter+=1
        
        if event.is_set():
            break
        sleep(10)

# text to speech

@bot.message_handler(commands=['tts', 'Text to speech'])

def tts_handler(message):

    try:    

        chat_id_check(message)

        stats.addCommand("tts",str(message.from_user.username))
        logger.command(message)

        text_message = message.reply_to_message # get replied message
        bot.delete_message(message.chat.id, message.id) # delete initial command

        response_message = bot.reply_to(text_message, 'Un secondo che devo parlare ai muri.',disable_notification=True) 

        event = Event()
        animator = Thread(target=text_voice_reply_animator, args=(response_message,event,))
        animator.start()

        try:
            # testo del messaggio
            text = text_message.text

            wav_audio_path = "temp/tts.wav"

            textToSpeech.text_to_speech(text,wav_audio_path)
            
            bot.send_voice(text_message.chat.id, open(wav_audio_path, 'rb'), reply_to_message_id=text_message.message_id,disable_notification=True)
                         
            logger.telegramMessage("Text to speech eseguito! Testo: "+text,message)
            
            event.set()
            animator.join()
            voiceRecognizer.clear(wav_audio_path)
            bot.delete_message(response_message.chat.id, response_message.id) # delete reply message

        except:
            event.set()
            animator.join()
            bot.edit_message_text(chat_id=response_message.chat.id, message_id=response_message.message_id, text="Errore. Questo non mi sembra testo!")

    except wrongChatID:
        logger.telegramError("wrongChatID",message)
        pass

def text_voice_reply_animator(response_message,event):

    text = "Un secondo che devo parlare ai muri.."
    counter = 0
    while True:
        
        if counter == 5:
            text = "Un secondo che devo parlare ai muri."
            counter = 0

        bot.edit_message_text(chat_id=response_message.chat.id, message_id=response_message.message_id, text=text)
        text +="."

        counter+=1
        
        if event.is_set():
            break
        sleep(3)

@bot.message_handler(commands=['ask', 'Chat with IA LLM'])
def ask_llm_handler(message):
    try:    

        chat_id_check(message)

        stats.addCommand("ask",str(message.from_user.username))
        logger.command(message)

        text_message = message.reply_to_message # get replied message
        bot.delete_message(message.chat.id, message.id) # delete initial command

        if client is None:
            if text_message:
                send_long_message(bot, text_message.chat.id, "GROQ_API_KEY non impostata nel file .env", disable_notification=True, reply_to_message_id=text_message.message_id)
            else:
                send_long_message(bot, message.chat.id, "GROQ_API_KEY non impostata nel file .env", disable_notification=True)
            return
            
        if text_message:
            response_message = bot.reply_to(text_message, 'Chiedendo a groq...',disable_notification=True) 
            text = text_message.text
            # Include context if the text_message is replying to another message
            if text_message.reply_to_message and text_message.reply_to_message.text:
                context = text_message.reply_to_message.text
                text = f"Context: {context}\n\n{text}"
        else:
            # Parse text from the command message (after "/ask ")
            command_prefix = "/ask "
            if message.text.startswith(command_prefix):
                text = message.text[len(command_prefix):].strip()
            else:
                text = message.text  # fallback
            response_message = bot.send_message(message.chat.id, 'Chiedendo a groq...', disable_notification=True)

        event = Event()
        animator = Thread(target=text_voice_reply_animator, args=(response_message,event,))
        animator.start()

        try:
            response = client.chat.completions.create(
                model=tokenManager.read_groq_model(),
                messages=[
                    {"role": "user", "content": text}
                ]
            )

            cleaned_content = clean_think_tags(response.choices[0].message.content)

            if text_message:
                send_long_message(bot, text_message.chat.id, cleaned_content, disable_notification=True, reply_to_message_id=text_message.message_id)
            else:
                send_long_message(bot, message.chat.id, cleaned_content, disable_notification=True)
                         
            logger.telegramMessage("IA LLM risposta eseguita! Testo: "+cleaned_content,message)
            
            event.set()
            animator.join()
            bot.delete_message(response_message.chat.id, response_message.id) # delete reply message

        except Exception as e:
            event.set()
            animator.join()
            bot.edit_message_text(chat_id=response_message.chat.id, message_id=response_message.message_id, text=f"Errore. {str(e)}")

    except wrongChatID:
        logger.telegramError("wrongChatID",message)
        pass

@bot.message_handler(commands=['patchnotes', 'Ottiene le ultime patch notes'])
def get_patchnotes(message):

    try:

        chat_id_check(message)

        stats.addCommand("patchnotes",str(message.from_user.username))
        logger.command(message)

        bot.delete_message(message.chat.id, message.id) # delete initial command

        f = open("data/patchnotes", "r") # reads and return entire file
        send_long_message(bot, message.chat.id, f.read(), disable_notification=True)

    except wrongChatID:
        logger.telegramError("wrongChatID",message)
        pass

@bot.message_handler(commands=['logs', 'Ritorna gli ultimi log del bot'])
def get_latestlogs(message):

    try:    

        chat_id_check(message)

        stats.addCommand("logs",str(message.from_user.username))
        logger.command(message)

        logs = logger.getLogs()

        send_long_message(bot, message.chat.id, logs, disable_notification=True)

    except wrongChatID:
        logger.telegramError("wrongChatID",message)
        pass

# print stats in a fantastic formatted message

@bot.message_handler(commands=['stats', 'Vedi le statistiche di utilizzo'])
def get_stats(message):
    try:

        chat_id_check(message)

        stats.addCommand("stats",str(message.from_user.username))
        logger.command(message)

        bot.delete_message(message.chat.id, message.id) # delete initial command

        send_long_message(bot, message.chat.id, stats.getStats(), disable_notification=True)

    except wrongChatID:
        logger.telegramError("wrongChatID",message)
        pass



# get every message sent (for statistic purpuse only)

@bot.message_handler(func=lambda message: True)
def stats_text(message):
    stats.addMessage(message.from_user.username)
# questo metodo deve stare in fondo, altrimenti tutto il resto non funzia e si frega tutti i messaggi

logger.toConsole("---------------------------------------------------")
logger.toConsole("Bot started!")

bot.polling() # bot start
