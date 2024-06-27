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