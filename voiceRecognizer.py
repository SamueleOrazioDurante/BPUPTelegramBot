import os
import subprocess

import json
import wave
from vosk import Model, KaldiRecognizer, SetLogLevel

# Set log level to 0 to suppress Vosk logs
SetLogLevel(0)

# Load the Italian model
model_path = "vosk-model-it-0.22"  # Change this to your model path

model = Model(model_path)


def voice_recognizer(language):

    subprocess.run(['ffmpeg', '-i', 'audio.ogg', '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', 'audio.wav', '-y'])  # formatting ogg file in to wav format
    text = 'Words not recognized.'
    
    try:

        with open("audio.wav", 'rb') as file:
            audio_data = file.read()

        recognizer = KaldiRecognizer(model, 16000)
        recognizer.AcceptWaveform(audio_data)
        result_json = recognizer.FinalResult()
        result = json.loads(result_json)
        text = result['text']

        clear()

    except Exception as e:
        print(str(e))
        clear()


    return text

def clear():
    # Remove unnecessary files
    files = ['audio.wav', 'audio.ogg']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
