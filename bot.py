import telebot
import os
import urllib.request
import json
import requests

file = open("key", "r") 
key = file.read()
file.close()

file = open("apikey", "r") 
APIKey = file.read()
file.close()

bot = telebot.TeleBot(key)

quality = "play"

def APIRequest(url):
    
    APIUrl = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
    payload = "-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"url\"\r\n\r\n"+url+"\r\n-----011000010111000001101001\r\nContent-Disposition: form-data; name=\"hd\"\r\n\r\n1\r\n-----011000010111000001101001--\r\n\r\n"
    headers = {
        "x-rapidapi-key": APIKey,
        "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com",
        "Content-Type": "multipart/form-data; boundary=---011000010111000001101001"
    }
    response = requests.post(APIUrl, data=payload, headers=headers)

### TEMPLATE RESPONSE
#    file = open("JSONDefaultResponse", "r") 
#    jsonTik = json.loads(file.read())
#    file.close()

    jsonTik = response.json()
    return jsonTik["data"][quality]

def log(text,message):
    print(f"{text} MessageID: {message.id} Message text: {message.text}")

@bot.message_handler(commands=['bersinator', 'help'])
def easteregg(message):
    bot.send_message(message.chat.id, "Coglione")
@bot.message_handler(commands=['valorant', 'help'])
def easteregg(message):
    bot.send_message(message.chat.id, "magna coglione")
@bot.message_handler(commands=['bissolimerda', 'help'])
def easteregg(message):
    bot.send_message(message.chat.id, "puttana")

    
@bot.message_handler(regexp="https://vm.tiktok.com/")
def tiktok_dl(message):
    
    log("Richiesta di download: ",message)
    url = message.text
    
    filename = "tiktok.mp4"
    try:
        urllib.request.urlretrieve(APIRequest(url), filename)
        
        sendVideo(message,filename,filename)
    except Exception as e:
        print("Errore:", str(e))

def sendVideo(message,file,title):
    with open(file, 'rb') as video:
        bot.send_video(message.chat.id, video)
    os.remove(file)
    log("Download eseguito",message)  


bot.polling()
