import datetime

import fileLogger

def toConsole(text): # print on console
    date = str(datetime.datetime.now())
    text = date + " - "+text
    print(text)
    toFile(text)

def log(text,message): # get all messages
    toConsole(f"{text} \n   MessageID: {message.id} \n   Message text: {message.text} \n   Message sender: {message.chat.username} \n   Chat ID: {message.chat.id}")

def error(text,message,isError): # get all errors
    if isError:
        toConsole(f"Errore: {text}")

def command(message): # get all commands
     log("Comando eseguito!",message)

def toFile(text): # write to a log file
    fileLogger.write(text)