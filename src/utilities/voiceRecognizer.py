import auth.tokenManager as tokenManager
import logger.logger as logger
from utilities.fileManager import clear

import os
import subprocess

from transformers import pipeline
from pydub import AudioSegment

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

    audio = AudioSegment.from_wav(wav_audio_path)
    segment_length = 30 * 1000  # 30 seconds in milliseconds
    segments = [audio[i:i + segment_length] for i in range(0, len(audio), segment_length)]
    
    for segment in segments:
        segment.export("temp/segment.wav", format="wav")
        try:
            result = pipe("temp/segment.wav", generate_kwargs={"language": f"{language}"})
            text += result["text"]

        except Exception as e:
            return "Errore, riprova più tardi: " + str(e)
    
    return text


def fromvideo_voice_recognizer(mp4_audio_path):

    wav_audio_path = "temp/audio.wav"
    subprocess.run(['ffmpeg', '-i', f'{mp4_audio_path}', '-vn','-acodec', 'pcm_s16le' , '-ar', '44100', '-ac', '2', f'{wav_audio_path}', '-y', '-hide_banner', '-loglevel', 'error'])  # formatting mp4 file in to wav format

    clear(mp4_audio_path)
    return voice_recognizer(wav_audio_path)

def fromaudio_voice_recognizer(ogg_audio_path):

    wav_audio_path = "temp/audio.wav"

    subprocess.run(['ffmpeg', '-i', f'{ogg_audio_path}', f'{wav_audio_path}', '-y', '-hide_banner', '-loglevel', 'error'])  # formatting ogg file in to wav format

    clear(ogg_audio_path)
    return voice_recognizer(wav_audio_path)


