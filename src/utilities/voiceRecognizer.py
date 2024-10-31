import auth.tokenManager as tokenManager
import logger.logger as logger
from utilities.fileManager import clear

import os
import subprocess

from transformers import pipeline

model = tokenManager.get_model()
language = tokenManager.get_language()

if(model == "small"):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    logger.toConsole("Loaded model: small")
elif(model == "large"):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
    logger.toConsole("Loaded model: large")
else:
    logger.toConsole("Voice recognizer: disabled")


def voice_recognizer(wav_audio_path):

    text = "Trascrizione: "

    try:
        text += pipe(wav_audio_path,generate_kwargs={"language": f"{language}"})["text"]
    except Exception as e:
        text = "Errore, riprova più tardi:"+ str(e)

    clear(wav_audio_path)
    return text


def fromvideo_voice_recognizer(mp4_audio_path):

    wav_audio_path = "temp/audio.wav"
    subprocess.run(['ffmpeg', '-i', f'{mp4_audio_path}', '-vn','-acodec', 'pcm_s16le' , '-ar', '44100', '-ac', '2', f'{wav_audio_path}', '-y'])  # formatting mp4 file in to wav format

    clear(mp4_audio_path)
    return voice_recognizer(wav_audio_path)

def fromaudio_voice_recognizer(ogg_audio_path):

    wav_audio_path = "temp/audio.wav"

    subprocess.run(['ffmpeg', '-i', f'{ogg_audio_path}', f'{wav_audio_path}', '-y'])  # formatting ogg file in to wav format

    clear(ogg_audio_path)
    return voice_recognizer(wav_audio_path)


