import os
import subprocess

from transformers import pipeline


pipe = pipeline("automatic-speech-recognition", model="ALM/whisper-it-small")


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
