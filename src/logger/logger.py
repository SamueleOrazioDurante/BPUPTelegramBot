
import datetime

import logger.fileLogger as fileLogger

def toFile(text): # write to a log file
    fileLogger.write(text)

def toConsole(text): # print on console
    date = str(datetime.datetime.now())
    text = date + " - "+text
    print(text)
    toFile(text)

def telegramMessage(text,message): # get all messages
    toConsole(f"{text} \n   MessageID: {message.id} \n   Message text: {message.text} \n   Message sender: {message.chat.username} \n   Chat ID: {message.chat.id}")

def telegramError(text,message):
    telegramMessage(f"ERRORE: {text}",message)

def command(message): # get all commands DA SISTEMATE
     telegramMessage("Comando eseguito!",message)

def envValue(name,value):
    toConsole(f"ENV: {name} -> {value}")

def apiRequest(url,error):
    if error == None:
        toConsole(f"API: {url}")
    else:
        toConsole(f"API: {url} -> {error}")

def stats(text):
    toConsole(f"STATS: {text}")