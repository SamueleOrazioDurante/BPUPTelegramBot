import logger.logger as logger

import os

def read_value(NAME,is_necessary):

    #read value from config.py file
    
    VALUE = os.environ.get(NAME)
    logger.envValue(NAME,VALUE)

    if VALUE is None:
        logger.toConsole(f"WARNING: {NAME} not provided in .env file")
        if is_necessary:
            raise f"ERROR: {NAME} not provided in .env file."

    return VALUE

def read_bot_token():

    return read_value("BOT_TOKEN",True)

def read_tiktok_token():

    return read_value("TIKTOK_API_TOKEN",False)

def read_twitter_token():

    return read_value("TWITTER_API_TOKEN",False)

def read_instagram_token():

    return read_value("INSTAGRAM_API_TOKEN",False)

def read_chat_id():
    
    return read_value("CHAT_ID",True)

def get_language():

    return read_value("LANGUAGE",False)

def get_model():

    return read_value("MODEL",False)

def read_welcome_message():

    return read_value("WELCOME_MESSAGE",False)

def read_stt_type():

    return read_value("TYPE",False)

def read_groq_api_key():

    return read_value("GROQ_API_KEY",False)

def read_groq_model():

    return read_value("GROQ_MODEL",False)