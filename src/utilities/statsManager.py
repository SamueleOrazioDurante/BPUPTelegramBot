import os, json
import logger.logger as logger

stats_path = 'data/stats/stats.json'

def init_dict():

    messages = {}

    totext = {}
    tts = {}
    patchnotes = {}
    logs = {}
    stats = {}

    commands = {
        "totext":totext,
        "tts":tts,
        "patchnotes":patchnotes,
        "logs":logs,
        "stats":stats
    }

    tiktok = {}
    twitter = {}
    instagram = {}

    apis = {
        "tiktok":tiktok,
        "twitter":twitter,
        "instagram":instagram

    }

    stats_dict = {
        "messages":messages,
        "commands":commands,
        "apis":apis
    }

    return stats_dict

def dumpToJSON(stats_dict):
    with open(stats_path, 'w') as outfile:
        json.dump(stats_dict, outfile)

# DA VEDERE SE AGGIUNGERE LA VALIDAZIONE


if not os.path.exists(stats_path):

    #INIT json file (if it doesnt exist)

    logger.stats("Inizializzazione file stats.json")
    stats_dict = init_dict()
    dumpToJSON(stats_dict)
    logger.stats("File stats.json creato!")

else:
    with open(stats_path, 'r') as file:
        stats_dict = json.load(file)

    logger.stats("File stats.json caricato nel dict!")


def checkIfUserExist(name,f_name,username):

    if (name == "apis") | (name == "commands"):
        for user in stats_dict[name][f_name]:
            if user == username:
                return True

        stats_dict[name][f_name].update({username:0}) # add username
        logger.stats(f"{username} created!")
        return True

    else:
        for user in stats_dict[name]:
            if user == username:
                return True

        stats_dict[name].update({username:0}) #add username
        logger.stats(f"{username} created!")
        return True
            

def updateDict(name,f_name,username):

    logger.stats(f"Richiesta a {name} -> {f_name} -> {username}")

    if checkIfUserExist(name,f_name,username):

        logger.stats("Aggiornamento del dict...")

        if (name == "apis") | (name == "commands"):
            counter = stats_dict[name][f_name][username] + 1
            stats_dict[name][f_name].update({username:counter})
        else:
            counter = stats_dict[name][username] + 1
            stats_dict[name].update({username:counter})

        print(stats_dict)
        dumpToJSON(stats_dict)
        
        logger.stats("JSON updated")

    else:
        return False # thro exc

def addAPIRequest(social,username):
    updateDict("apis",social,username)

def addCommand(command,username):
    updateDict("commands",command,username)

def addMessage(username):
    updateDict("messages","easteregg??",username)

# Funzione per formattare i dati dinamicamente
def format_data(data, indent=0):
    formatted_output = ""
    for key, value in data.items():
        if isinstance(value, dict):  # Se il valore è un dizionario, esplora ricorsivamente
            formatted_output += " " * indent + f"{key}:\n"
            formatted_output += format_data(value, indent + 4)
        else:  # Altrimenti, stampa la chiave e il valore
            formatted_output += " " * indent + f"{key}: {value}\n"
    return formatted_output
    
def getStats():

    # Formattazione dinamica dei dati
    formatted_data = format_data(stats_dict)

    text = "Riepilogo delle statistiche di utilizzo:\n"
    text += formatted_data

    return text