import logger.logger as logger

import os

def read_value(NAME):

    #read value from config.py file
    
    VALUE = os.environ.get(NAME)
    logger.envValue(NAME,VALUE)

    if VALUE is None:
        logger.toConsole(NAME+" not provided in .env file")
        raise "Parameter not provided"
    return VALUE

def read_bot_token():

    return read_value("BOT_TOKEN")

def read_tiktok_token():

    return read_value("TIKTOK_API_TOKEN")

def read_twitter_token():

    return read_value("TWITTER_API_TOKEN")

def read_instagram_token():

    return read_value("INSTAGRAM_API_TOKEN")

def read_chat_id():
    
    return read_value("CHAT_ID")

def get_language():

    return read_value("LANGUAGE")

def get_model():

    return read_value("MODEL")

