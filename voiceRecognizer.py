import os
import subprocess

import whisper

model = whisper.load_model('base')

def voice_recognizer(language):

    subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])  # formatting ogg file in to wav format
    text = 'Words not recognized.'

    path = "audio.wav"

    try:
        result = model.transcribe(str(path), language=language, verbose=False)  # listen to file
        text = result['text']  # and write the heard text to a text variable
    except Exception as e:
        print(str(e))

    return text

def clear():
    # Remove unnecessary files
    files = ['audio.wav', 'audio.ogg']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
