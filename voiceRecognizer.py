import os
import subprocess
import re

import whisper

whisper_model = whisper.load_model("small") #+ ("." + "it"))

def voice_recognizer():

    result = whisper_model.transcribe("audio.wav", verbose=False, language=language, fp16=False)
    rawtext = " ".join([segment["text"].strip() for segment in result["segments"]])  # type: ignore
    rawtext = re.sub(" +", " ", rawtext)
    alltext = re.sub(r"([\.\!\?]) ", r"\1\n", rawtext)

    clear()

    return alltext


def clear():
    # Remove unnecessary files
    files = ['audio.wav', 'audio.ogg']
    for file in files:
        if os.path.exists(file):
            os.remove(file)
