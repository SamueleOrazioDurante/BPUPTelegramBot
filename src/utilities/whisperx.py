import whisperx
import gc
import logger.logger as logger
from utilities.fileManager import clear

import os
import queue
import threading
import warnings

# Suppress cpuinfo warnings (for ARM devices)
warnings.filterwarnings("ignore", category=UserWarning, module="cpuinfo")

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

device = "cpu"  # Use CPU instead of GPU
batch_size = 16
compute_type = "float32"  # Use float32 for CPU processing

model = None  # Lazy load the model

def get_model():
    global model
    if model is None:
        logger.toConsole("Loading WhisperX model...")
        model = whisperx.load_model("large-v2", device, compute_type=compute_type)
        logger.toConsole("WhisperX model loaded.")
    return model

# Thread worker che processa le richieste nella coda
def transcription_worker():
    global is_processing
    logger.toConsole("Transcription worker started")
    
    while True:
        try:
            task = transcription_queue.get()
            if task is None:  # Segnale di stop
                break
                
            with processing_lock:
                is_processing = True
                queue_status["current_position"] += 1
            
            audio_path, audio_type, callback = task
            
            if audio_type in ["audio", "video"]:
                result = process_audio(audio_path)
            else:
                result = "Formato non supportato"
            
            callback(result)
            transcription_queue.task_done()
            queue_status["processed_requests"] += 1
            
            with processing_lock:
                is_processing = False
            
            logger.toConsole(f"Task processed. Remaining in queue: {transcription_queue.qsize()}")
            
        except Exception as e:
            logger.toConsole(f"Error in transcription worker: {str(e)}")
            with processing_lock:
                is_processing = False

worker_thread = threading.Thread(target=transcription_worker, daemon=True)
worker_thread.start()

def queue_transcription_request(audio_path, audio_type, callback):
    global queue_status
    
    queue_status["total_requests"] += 1
    position = transcription_queue.qsize() + (1 if is_processing else 0)
    transcription_queue.put((audio_path, audio_type, callback))
    
    logger.toConsole(f"Request added to queue. Position: {position}")
    return position

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

def process_audio(audio_path):
    try:
        logger.toConsole(f"Processing audio: {audio_path}")
        model = get_model()  # Lazy load the model
        audio = whisperx.load_audio(audio_path)
        result = model.transcribe(audio, batch_size=batch_size)
        
        # Align transcription
        model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        
        # Clean up memory
        gc.collect()
        del model_a
        
        # Format transcription result
        transcription = "Trascrizione:\n"
        for segment in result["segments"]:
            transcription += f"{segment['text']}\n"
        
        clear(audio_path)
        return transcription
    
    except Exception as e:
        logger.toConsole(f"Error in audio processing: {str(e)}")
        return f"Errore, riprova più tardi: {str(e)}"