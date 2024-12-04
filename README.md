# Telegram bot

*PROGETTO ABBANDONATO* -> mi sto attualmente concetrando sull`uni e su BPUP Messanger :D
anche se ogni tanto faccio dei mini fix a dei bug che trovo in giro

NON AGGIORNATO

Questo progetto contiene un bot di telegram scritto totalmente in python e predisposto per l'esecuzione in Docker.
Utilizzato per un gruppo privato. 

# Feature
Tiktok Video Download

X (Twitter) Post Download

Speech to text tramite comando /totext in risposta ad un messaggio audio


Comandi a caso


TODS:

  -------------------------------------------------------------------
  
  - E con questo ci si prepare alla versione 1.2 che avrà: (predicto cosa penso riuscirò a fare) 

    1) Nuovo model più veloce (super fast whisper) per la trascrizione audio
      (da vedere anche la precisione di questo model, casomai sarebbe da capire se posso cambiare model in mezzo all'esecuzione così da scaricare quello italiano che uso adesso [SUPER PRECISO] ed eventualmente cambiare al super fast whisper o altri large model anche per le funzioni che vorrei inserire, elencate sotto)
    2) Separazione degli audio in più blocchi (da tot. MB che ancora non so) per la trascrizione di audio di durata (VIRTUALMENTE) infinita (da vedere se sarebbe utile usare thread separati, anche se dubito visto che hosto sto coso su una povera VPS di oracle [quella da 4 core arm e 24 gb di ram che non so come faccia a essere viva dopo tutti gli anni di abuso subito dalla mia voglia di provare questi super model, una volta gli ho anche provato ad installare ollama 3.2 90b e mi son pentito] )
    3) (E se quelli due sopra funzionano bene) supporto per un grande numero di lingue (di cui farò liste nelle impostazioni)
    4) Menù delle impostazioni per il setting della qualità dei video scaricati e la gestione della lingua di STT e TTS
    5) Utilizzo di model anche per il TTS (attualmente usa una bruttissima e vecchissima libreria che non voglio mai più vedere)
    6) Possibilità di inizializzare il bot senza scaricare model per migliorare la velocità di esecuzione (sia per tts che per stt) con relativo messaggio di avviso
    7) Possibilità di inizializzare il bot senza api key delle varie api usate da RapidAPI sempre con relativo messaggio di avviso
    8) Cosa che mi è venuta in mente 5 minuti dopo aver committato: aggiungere un messaggio che stima il tempo di trascrizione di un messaggio (sostituito a quella specie di animazione che ho provato a fare con i puntini, quindi almeno con i secondi che scendono)
    9) a quanto pare le patchnotes ora sono anche troppo lunghe, quindi me tocca capire come fare a mandarle su telegram (probabilmente finirò per fare un messaggio splittato in tot caratteri e da cui potrai spostarti usando le freccettine dei markup, da vedere poi come studiarla sta roba dio povero)

    ALTRE COSE DA FARE:
    sistema la sezione logger (relativo a comandi)
    rivedi il sistema di log (per loggare TUTTI i comandi, in modo efficiente)
    rivedi il sistema della ricezione dei comandi
    rivedi le eccezioni (TUTTE) per printarne gli errori nel file log
    aggiungi data.ora.minuto.secondo.ms al nome di un file per renderlo unico ed evitare alcuni spiacevoli bug con la concorrenza (poi da eliminare anche il file alla fine dell`utilizzo, sopratutto audio + segment)
    rivedi la parte relativa al voiceRecognizer per far in modo che se il modello non è stato scelto, allora non funziona il recognizer (tral'altro servirà anche pensare a salvare il model e altri config in locale anche dopo che il bot viene spento altrimento son cassi)

    *EOF*
