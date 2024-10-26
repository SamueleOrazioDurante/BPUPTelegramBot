import auth.tokenManager as tokenManager
import logger.logger as logger

import pyttsx3

TTS_ENGINE = pyttsx3.init()

voices = TTS_ENGINE.getProperty('voices') 

# da aggiungere all`env se voce maschile 0 femminile o anche lingua diversa
for voice in voices:

    if voice.languages[0] == 'it':
        TTS_ENGINE.setProperty('voice', voice.id)
        #print(voice)
        break

logger.toConsole("TTS: Init done")

def text_to_speech(text,fileName):

    logger.toConsole("TTS: Inizio elaborazione")
    TTS_ENGINE.save_to_file(text, fileName)
    TTS_ENGINE.runAndWait()
    logger.toConsole("TTS: Fine")