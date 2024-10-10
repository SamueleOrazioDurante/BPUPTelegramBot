import os
import subprocess

from transformers import pipeline

# Crea il pipeline per il riconoscimento automatico del parlato
pipe = pipeline("automatic-speech-recognition", model="ALM/whisper-it-small")

def voice_recognizer(language):

    subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])  # formatting ogg file in to wav format
    text = 'Words not recognized.'


    try:

        # Specifica il percorso del file audio
        audio_file = "audio.wav"

        # Trasforma il file audio in testo
        result = pipe(audio_file)

        # Stampa il risultato
        text = result['text']

    except Exception as e:
        print(str(e))

    return text

def clear():
    # Remove unnecessary files
    files = ['audio.wav', 'audio.ogg']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
