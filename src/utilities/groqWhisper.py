import auth.tokenManager as tokenManager
import logger.logger as logger
from utilities.fileManager import clear

import os
import subprocess
import queue
import threading
from groq import Groq

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

language = tokenManager.get_language()
# fallback language to english if not set
if not language:
    language = "en"

groq_api_key = tokenManager.read_groq_api_key()
if groq_api_key:
    client = Groq(api_key=groq_api_key)
    logger.toConsole("Groq STT client initialized.")
else:
    client = None
    logger.toConsole("WARNING: Groq API key not provided, STT will not work.")

# Thread worker che processa le richieste nella coda
def transcription_worker():
    global is_processing
    logger.toConsole("Groq Transcription worker started")
    
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
            logger.toConsole(f"Error in Groq transcription worker: {str(e)}")
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
    
    logger.toConsole(f"Request added to Groq queue. Position: {position}")
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
    if not client:
        return "Groq API non configurata."

    logger.toConsole("STT: Inizio trascrizione con Groq (whisper-large-v3-turbo)")
    
    try:
        with open(wav_audio_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(wav_audio_path), file.read()),
                model="whisper-large-v3-turbo",
            )
        
        clear(wav_audio_path)
        return "Trascrizione: " + transcription.text
    except Exception as e:
        clear(wav_audio_path)
        return "Errore, riprova più tardi: " + str(e)

def fromvideo_voice_recognizer(mp4_audio_path):
    wav_audio_path = f"temp/audio_{os.path.basename(mp4_audio_path)}.wav"
    subprocess.run(['ffmpeg', '-i', f'{mp4_audio_path}', '-vn','-acodec', 'pcm_s16le' , '-ar', '44100', '-ac', '2', f'{wav_audio_path}', '-y', '-hide_banner', '-loglevel', 'error'])
    clear(mp4_audio_path)
    return voice_recognizer(wav_audio_path)

def fromaudio_voice_recognizer(ogg_audio_path):
    wav_audio_path = f"temp/audio_{os.path.basename(ogg_audio_path)}.wav"
    subprocess.run(['ffmpeg', '-i', f'{ogg_audio_path}', f'{wav_audio_path}', '-y', '-hide_banner', '-loglevel', 'error'])
    clear(ogg_audio_path)
    return voice_recognizer(wav_audio_path)
