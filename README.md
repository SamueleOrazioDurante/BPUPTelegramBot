*PROGETTO ABBANDONATO* -> mi sto attualmente concetrando sull`uni e sulla'app di messagistica :D
anche se ogni tanto faccio dei mini fix a dei bug che trovo in giro
Below is a comprehensive, bilingual (English and Italian) documentation draft for the BPUPTelegramBot repository. You can copy the content into a README.md file in your repository. Adjust details as needed to reflect your project’s specifics.

---

# BPUPTelegramBot Documentation

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [Documentazione in Italiano](#documentazione-in-italiano)

---

## Introduction
  
BPUPTelegramBot is a Telegram bot designed to streamline interactions on Telegram by offering automated commands, notifications, and additional functionalities. Built with simplicity and flexibility in mind, this bot can be easily extended and customized to suit a variety of needs.

**Key aspects include:**  
- Lightweight and modular design  
- Easy installation and configuration  
- Ready-to-use commands and functionality  

---

## Installation
  
To install BPUPTelegramBot, follow these steps:

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/SamueleOrazioDurante/BPUPTelegramBot.git
   cd BPUPTelegramBot
   ```

2. **Install Dependencies:**  
   Ensure you have Python (3.6+) installed. Then, install required libraries:  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Your Bot:**  
   Obtain a Telegram Bot token from [BotFather](https://t.me/BotFather) and add it to your configuration file or environment variables.

4. **Run the Bot:**  
   Start the bot by running:
   ```bash
   python bot.py
   ```

---

## Configuration

- **Environment Variables:**  
  Set your bot token and any other necessary configuration (e.g., admin IDs, command prefixes) in your environment or in a configuration file (e.g., `config.json`).

- **Customization:**  
  Modify the command handlers in the codebase to add new functionalities or alter existing commands.

---

## Usage

After installation, invite your bot to a Telegram chat or group. Use the following commands to interact:

- `/start` – Initializes the bot and displays a welcome message.  
- `/help` – Shows available commands and usage instructions.  
- *Other commands* – Refer to the source code and configuration for further command details.

You can also extend the functionality by creating new command modules as described in the code documentation.

---

## Features

- **Automated Command Handling:**  
  Simplify common tasks with ready-to-use commands.
- **Modular Design:**  
  Easily extend or modify the bot’s functionality by adding or editing modules.
- **Notification System:**  
  Configurable notifications for events, reminders, or updates.
- **Customizable Settings:**  
  Change command prefixes, access controls, and other parameters with minimal effort.

## Documentazione in Italiano

### Indice

- [Introduzione](#introduzione)
- [Installazione](#installazione)
- [Configurazione](#configurazione)
- [Utilizzo](#utilizzo)
- [Caratteristiche](#caratteristiche)

---

### Introduzione

BPUPTelegramBot è un bot per Telegram progettato per semplificare le interazioni tramite comandi automatici, notifiche e funzionalità aggiuntive. Realizzato con un’architettura modulare e flessibile, il bot è facilmente personalizzabile per adattarsi a diverse esigenze.

**Aspetti chiave:**  
- Design leggero e modulare  
- Installazione e configurazione semplici  
- Comandi pronti all’uso e funzionalità estendibili

---

### Installazione

Per installare BPUPTelegramBot, segui questi passaggi:

1. **Clona il Repository:**  
   ```bash
   git clone https://github.com/SamueleOrazioDurante/BPUPTelegramBot.git
   cd BPUPTelegramBot
   ```

2. **Installa le Dipendenze:**  
   Assicurati di avere Python (3.6+) installato, poi installa le librerie necessarie:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura il Bot:**  
   Ottieni un token per il bot da [BotFather](https://t.me/BotFather) e aggiungilo alle variabili d’ambiente o nel file di configurazione.

4. **Avvia il Bot:**  
   Esegui il bot con:
   ```bash
   python bot.py
   ```

---

### Configurazione
  
- **Variabili d’Ambiente:**  
  Imposta il token del bot e altre configurazioni necessarie (es. ID degli admin, prefissi dei comandi) tramite variabili d’ambiente o in un file di configurazione (ad esempio `config.json`).

- **Personalizzazione:**  
  Modifica i gestori dei comandi nel codice per aggiungere nuove funzionalità o modificare quelle esistenti.

---

### Utilizzo

Una volta installato, invita il bot in una chat o in un gruppo Telegram. Utilizza i seguenti comandi per interagire:

- `/start` – Avvia il bot e mostra un messaggio di benvenuto.  
- `/help` – Mostra i comandi disponibili e le istruzioni d’uso.  
- *Altri comandi* – Consulta il codice sorgente e la configurazione per ulteriori dettagli sui comandi.

È possibile estendere le funzionalità creando nuovi moduli per i comandi come descritto nella documentazione del codice.

---

### Caratteristiche

- **Gestione Automatica dei Comandi:**  
  Semplifica le attività comuni grazie a comandi pronti all’uso.
- **Design Modulare:**  
  Facilmente estendibile o modificabile aggiungendo o editando moduli.
- **Sistema di Notifiche:**  
  Notifiche configurabili per eventi, promemoria o aggiornamenti.
- **Impostazioni Personalizzabili:**  
  Cambia prefissi dei comandi, controlli di accesso e altri parametri con facilità.


OLD DOCS:

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
