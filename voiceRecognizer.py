import os
import subprocess
import re

from whisper.model import Whisper
from whisper import load_model


def voice_recognizer(language):
    whisper_model = config.whisper_model + ("." + language)

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
