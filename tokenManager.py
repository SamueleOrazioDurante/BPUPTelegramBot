import os

def read_bot_token():

    #read bot token from config.py file
    BOT_TOKEN = None

    try:
        from config import BOT_TOKEN
    except:
        pass

    if len(BOT_TOKEN) == 0:
        BOT_TOKEN = os.environ.get('BOT_TOKEN')

    if BOT_TOKEN is None:
        raise ('Token for the bot must be provided (BOT_TOKEN variable)')
    return BOT_TOKEN

def read_tiktok_token():

    #read bot token from config.py file
    TIKTOK_API_TOKEN = None

    try:
        from config import TIKTOK_API_TOKEN
    except:
        pass

    if len(TIKTOK_API_TOKEN) == 0:
        TIKTOK_API_TOKEN = os.environ.get('TIKTOK_API_TOKEN')

    if TIKTOK_API_TOKEN is None:
        raise ('Token for the bot must be provided (TIKTOK_API_TOKEN variable)')
    return TIKTOK_API_TOKEN

def read_twitter_token():

    #read bot token from config.py file
    TWITTER_API_TOKEN = None

    try:
        from config import TWITTER_API_TOKEN
    except:
        pass

    if len(TWITTER_API_TOKEN) == 0:
        TWITTER_API_TOKEN = os.environ.get('TWITTER_API_TOKEN')

    if TWITTER_API_TOKEN is None:
        raise ('Token for the bot must be provided (TWITTER_API_TOKEN variable)')
    return TWITTER_API_TOKEN

def read_instagram_token():

    #read bot token from config.py file
    INSTAGRAM_API_TOKEN = None

    try:
        from config import INSTAGRAM_API_TOKEN
    except:
        pass

    if len(INSTAGRAM_API_TOKEN) == 0:
        INSTAGRAM_API_TOKEN = os.environ.get('INSTAGRAM_API_TOKEN')

    if INSTAGRAM_API_TOKEN is None:
        raise ('Token for the bot must be provided (INSTAGRAM_API_TOKEN variable)')
    return INSTAGRAM_API_TOKEN

def read_chat_id():

    #read chat_id from config.py file
    CHAT_ID = None

    try:
        from config import CHAT_ID
    except:
        pass

    if len(CHAT_ID) == 0:
        CHAT_ID = os.environ.get('CHAT_ID')

    if CHAT_ID is None:
        raise ('Chat id for the bot must be provided (CHAT_ID variable)')
    return CHAT_ID

def get_language():

    #read model language from config.py file
    LANGUAGE = None

    try:
        from config import LANGUAGE
    except:
        pass

    if len(LANGUAGE) == 0:
        LANGUAGE = os.environ.get('LANGUAGE')

    if LANGUAGE is None:
        raise ('Model language for the bot must be provided (LANGUAGE variable)')
    return LANGUAGE

def get_model():

    #read model type from config.py file
    MODEL = None

    try:
        from config import MODEL
    except:
        pass

    if len(MODEL) == 0:
        MODEL = os.environ.get('MODEL')

    if MODEL is None:
        raise ('Model type for the bot must be provided (MODEL variable)')
    return MODEL

