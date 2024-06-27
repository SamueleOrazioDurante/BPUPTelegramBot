import os
import subprocess

def voice_recognizer(sr,language):

    recognizer = sr.Recognizer()

    subprocess.run(['ffmpeg', '-i', 'audio.ogg', 'audio.wav', '-y'])  # formatting ogg file in to wav format
    text = 'Words not recognized.'
    file = sr.AudioFile('audio.wav')
    with file as source:
        try:
            audio = recognizer.record(source)  # listen to file
            text = recognizer.recognize_google(audio, language=language)  # and write the heard text to a text variable
        except Exception as e:
            print(str(e))

    return text

def clear():
    # Remove unnecessary files
    files = ['audio.wav', 'audio.ogg']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
