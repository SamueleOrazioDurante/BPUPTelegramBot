import auth.tokenManager as tokenManager
import logger.logger as logger
from utilities.fileManager import clear

import os
import subprocess
import queue
import threading
import time

from transformers import pipeline
from pydub import AudioSegment

# Crea una coda per le richieste di trascrizione
transcription_queue = queue.Queue()
processing_lock = threading.Lock()
is_processing = False

# Informazioni sulla coda
queue_status = {
    "total_requests": 0,
    "processed_requests": 0,
    "current_position": 0
}

model = tokenManager.get_model()
language = tokenManager.get_language()

logger.toConsole(f"Voice recognizer model: {model}")

if(model == "small"):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-small")
    logger.toConsole("Loaded model: small")
elif(model == "large"):
    pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
    logger.toConsole("Loaded model: large")
else:
    pipe = None
    logger.toConsole("Voice recognizer: disabled")

# Thread worker che processa le richieste nella coda
def transcription_worker():
    global is_processing
    logger.toConsole("Transcription worker started")
    
    while True:
        try:
            # Attende un elemento nella coda
            task = transcription_queue.get()
            if task is None:  # Segnale di stop
                break
                
            with processing_lock:
                is_processing = True
                queue_status["current_position"] += 1
            
            # Estrae i dati del task
            audio_path, audio_type, callback = task
            
            # Processa la richiesta in base al tipo
            if audio_type == "audio":
                result = fromaudio_voice_recognizer(audio_path)
            elif audio_type == "video":
                result = fromvideo_voice_recognizer(audio_path)
            else:
                result = "Formato non supportato"
            
            # Chiama la callback con il risultato
            callback(result)
            
            # Segna il task come completato
            transcription_queue.task_done()
            queue_status["processed_requests"] += 1
            
            with processing_lock:
                is_processing = False
            
            logger.toConsole(f"Task processed. Remaining in queue: {transcription_queue.qsize()}")
            
        except Exception as e:
            logger.toConsole(f"Error in transcription worker: {str(e)}")
            with processing_lock:
                is_processing = False

# Avvia il worker thread
worker_thread = threading.Thread(target=transcription_worker, daemon=True)
worker_thread.start()

# Aggiunge una richiesta alla coda
def queue_transcription_request(audio_path, audio_type, callback):
    global queue_status
    
    queue_status["total_requests"] += 1
    position = transcription_queue.qsize() + (1 if is_processing else 0)
    
    # Aggiunge il task alla coda
    transcription_queue.put((audio_path, audio_type, callback))
    
    logger.toConsole(f"Request added to queue. Position: {position}")
    return position

# Ottiene lo stato della coda
def get_queue_status():
    with processing_lock:
        position = transcription_queue.qsize()
        is_busy = is_processing
    
    return {
        "position": position,
        "is_busy": is_busy,
        "total_processed": queue_status["processed_requests"],
        "current_position": queue_status["current_position"]
    }

def voice_recognizer(wav_audio_path):
    if not pipe:
        return "Voice recognition is disabled"

    text = "Trascrizione: "

    audio = AudioSegment.from_wav(wav_audio_path)
    segment_length = 30 * 1000  # 30 seconds in milliseconds
    segments = [audio[i:i + segment_length] for i in range(0, len(audio), segment_length)]
    
    logger.toConsole("STT: Inizio trascrizione")
    for segment in segments:
        segment_path = "temp/segment.wav"
        segment.export(segment_path, format="wav")
        try:
            result = pipe(segment_path, generate_kwargs={"language": f"{language}"})
            text += result["text"]
            clear(segment_path)

        except Exception as e:
            return "Errore, riprova più tardi: " + str(e)
    
    clear(wav_audio_path)
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