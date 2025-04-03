import auth.tokenManager as tokenManager
import logger.logger as logger
from utilities.fileManager import clear

import os
import subprocess
import json
import wave
import queue
import threading
import time
import requests
import zipfile
import shutil

from vosk import Model, KaldiRecognizer
from pydub import AudioSegment

# URL dei modelli Vosk per l'italiano
MODEL_URLS = {
    "small": "https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip",
    "large": "https://alphacephei.com/vosk/models/vosk-model-it-0.22.zip"
}

# Funzione per scaricare e installare un modello
def download_model(model_type):
    if model_type not in MODEL_URLS:
        logger.toConsole(f"Modello '{model_type}' non disponibile")
        return False
    
    url = MODEL_URLS[model_type]
    model_filename = os.path.basename(url)
    download_path = os.path.join("temp", model_filename)
    extract_dir = os.path.join("models")
    
    # Crea la directory temp se non esiste
    os.makedirs("temp", exist_ok=True)
    
    logger.toConsole(f"Downloading {model_type} model from {url}...")
    
    try:
        # Scarica il file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Verifica errori HTTP
        
        # Salva il file zip
        with open(download_path, 'wb') as f:
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            chunk_size = 8192
            
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    # Mostra progresso
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        if percent % 10 == 0:  # Mostra solo ogni 10%
                            logger.toConsole(f"Download progress: {percent:.1f}%")
        
        logger.toConsole(f"Download completed. Extracting...")
        
        # Estrai il file zip
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            # Ottieni il nome della directory principale nel zip
            root_dirs = {item.split('/')[0] for item in zip_ref.namelist() if '/' in item}
            if len(root_dirs) == 1:
                main_dir = root_dirs.pop()
                # Estrai nella directory temporanea
                temp_extract = os.path.join("temp", "extracted")
                os.makedirs(temp_extract, exist_ok=True)
                zip_ref.extractall(temp_extract)
                
                # Sposta nella directory finale con il nome corretto
                if model_type == "small":
                    target_dir = os.path.join(extract_dir, "vosk-model-small-it")
                else:
                    target_dir = os.path.join(extract_dir, "vosk-model-it")
                
                if os.path.exists(target_dir):
                    shutil.rmtree(target_dir)
                
                shutil.move(os.path.join(temp_extract, main_dir), target_dir)
                shutil.rmtree(temp_extract)
            else:
                # Estrai direttamente
                zip_ref.extractall(extract_dir)
        
        # Rimuovi il file zip
        os.remove(download_path)
        logger.toConsole(f"Model {model_type} installed successfully")
        return True
        
    except Exception as e:
        logger.toConsole(f"Error downloading model: {str(e)}")
        # Cleanup in caso di errore
        if os.path.exists(download_path):
            os.remove(download_path)
        return False

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

model_name = tokenManager.get_model()
language = tokenManager.get_language()

# Path where Vosk models will be stored
model_path = "models"
if not os.path.exists(model_path):
    os.makedirs(model_path)

# Define model paths based on size
small_model_path = os.path.join(model_path, "vosk-model-small-it")
large_model_path = os.path.join(model_path, "vosk-model-it")

# Initialize model based on configuration
if model_name == "small":
    if not os.path.exists(small_model_path):
        logger.toConsole("Downloading small Italian Vosk model...")
        if download_model("small"):
            model = Model(small_model_path)
            logger.toConsole("Loaded Vosk model: small (Italian)")
        else:
            model = None
            logger.toConsole("Failed to download model. Voice recognition disabled.")
    else:
        model = Model(small_model_path)
        logger.toConsole("Loaded Vosk model: small (Italian)")
elif model_name == "large":
    if not os.path.exists(large_model_path):
        logger.toConsole("Downloading large Italian Vosk model...")
        if download_model("large"):
            model = Model(large_model_path)
            logger.toConsole("Loaded Vosk model: large (Italian)")
        else:
            model = None
            logger.toConsole("Failed to download model. Voice recognition disabled.")
    else:
        model = Model(large_model_path)
        logger.toConsole("Loaded Vosk model: large (Italian)")
else:
    model = None
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
    if not model:
        return "Voice recognition is disabled"

    text = "Trascrizione: "
    
    logger.toConsole("STT: Inizio trascrizione")
    
    try:
        wf = wave.open(wav_audio_path, "rb")
        
        # Check if the audio format is compatible with Vosk
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            # Convert to the required format if necessary
            audio = AudioSegment.from_wav(wav_audio_path)
            audio = audio.set_channels(1)  # Mono
            audio = audio.set_sample_width(2)  # 16-bit
            temp_path = "temp/converted.wav"
            audio.export(temp_path, format="wav")
            wf.close()
            wf = wave.open(temp_path, "rb")
        
        rec = KaldiRecognizer(model, wf.getframerate())
        rec.SetWords(True)
        
        # Process audio in chunks
        chunk_size = 4000
        while True:
            data = wf.readframes(chunk_size)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "text" in result:
                    text += result["text"] + " "
        
        # Get final result
        result = json.loads(rec.FinalResult())
        if "text" in result:
            text += result["text"]
        
        wf.close()
        clear(wav_audio_path)
        
        return text
    
    except Exception as e:
        logger.toConsole(f"Error in voice recognition: {str(e)}")
        return "Errore, riprova più tardi: " + str(e)


def fromvideo_voice_recognizer(mp4_audio_path):
    wav_audio_path = "temp/audio.wav"
    # Convert to mono 16kHz 16bit PCM for better results with Vosk
    subprocess.run(['ffmpeg', '-i', f'{mp4_audio_path}', '-vn', '-acodec', 'pcm_s16le', 
                   '-ar', '16000', '-ac', '1', f'{wav_audio_path}', '-y', 
                   '-hide_banner', '-loglevel', 'error'])

    clear(mp4_audio_path)
    return voice_recognizer(wav_audio_path)


def fromaudio_voice_recognizer(ogg_audio_path):
    wav_audio_path = "temp/audio.wav"
    # Convert to mono 16kHz 16bit PCM for better results with Vosk
    subprocess.run(['ffmpeg', '-i', f'{ogg_audio_path}', '-acodec', 'pcm_s16le',
                   '-ar', '16000', '-ac', '1', f'{wav_audio_path}', '-y',
                   '-hide_banner', '-loglevel', 'error'])

    clear(ogg_audio_path)
    return voice_recognizer(wav_audio_path)