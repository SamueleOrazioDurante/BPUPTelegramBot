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
recognizer = KaldiRecognizer(model, 16000)


def voice_recognizer(language):

    subprocess.run(['ffmpeg', '-i', 'audio.ogg', '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', 'audio.wav', '-y'])  # formatting ogg file in to wav format
    text = 'Words not recognized.'
    
    try:

        # Open a WAV file (you can also modify this to use a microphone)
        wf = wave.open("audio.wav", "rb")  # Change to your audio file path
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
            print("Audio file must be WAV format mono PCM.")
            return text

        # Read audio data and transcribe
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("partial", "")
            else:
                text = json.loads(recognizer.PartialResult()).get("partial", "")

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
