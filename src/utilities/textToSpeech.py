import auth.tokenManager as tokenManager
import logger.logger as logger

import requests

import wave
from piper.voice import PiperVoice

tts_model_name="it_IT-paola-medium"


# TEST, DOPO METTO UNA LISTA CON TUTTI I MODEL DISPONIBILI :D

model = f"./model/tts/model.onnx"

url = 'https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/paola/medium/it_IT-paola-medium.onnx?download=true'
r = requests.get(url, allow_redirects=True)

open(model, 'wb').write(r.content)

voice = PiperVoice.load(model)

logger.toConsole("TTS: Init done")

def text_to_speech(text,fileName):

    logger.toConsole("TTS: Inizio elaborazione")

    wav_file = wave.open(fileName, "w")
    audio = voice.synthesize(text, wav_file)

    logger.toConsole("TTS: Fine")