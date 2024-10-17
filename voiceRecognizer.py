import tokenManager, logger

import os
import subprocess

from transformers import pipeline


if(tokenManager.get_language() == "italian"):
    if(tokenManager.get_model() == "small"):
        pipe = pipeline("automatic-speech-recognition", model="ALM/whisper-it-small")
        logger.toConsole("Loaded model: italian-small")
    else:
        pipe = pipeline("automatic-speech-recognition", model="EdoAbati/whisper-large-v2-it")
        logger.toConsole("Loaded model: italian-large")
elif(tokenManager.get_model() == "small"):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    logger.toConsole("Loaded model: small")
elif(tokenManager.get_model() == "large"):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
    logger.toConsole("Loaded model: large")
else:
    pipe = pipeline("automatic-speech-recognition", model="distil-whisper/distil-large-v3")
    logger.toConsole("Loaded model: distil-large")


def voice_recognizer(language):

    subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])  # formatting ogg file in to wav format

    try:
        text = pipe("audio.wav")["text"]
    except:
        clear()
        return "Errore, riprova più tardi."

    clear()
    return text


def clear():
    # Remove unnecessary files
    files = ['audio.wav', 'audio.ogg']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
