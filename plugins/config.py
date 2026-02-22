import os
from os import environ, getenv
import logging

logging.basicConfig(
    format='%(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO
)

class Config(object):
    
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8176469571:AAH1c-BTNVwKp60FSOcKK6UPkdmksB2UGFE")
    API_ID = int(os.environ.get("API_ID", "23274996" ))
    API_HASH = os.environ.get("API_HASH", "7fa0c48ef9e57f8d92dba33ed6771e64")
    
    DOWNLOAD_LOCATION = "./DOWNLOADS"
    MAX_FILE_SIZE = 2194304000
    TG_MAX_FILE_SIZE = 2194304000
    FREE_USER_MAX_FILE_SIZE = 2194304000
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 128))
    DEF_THUMB_NAIL_VID_S = os.environ.get("DEF_THUMB_NAIL_VID_S", "")
    HTTP_PROXY = os.environ.get("HTTP_PROXY", "")
    
    OUO_IO_API_KEY = ""
    MAX_MESSAGE_LENGTH = 4096
    PROCESS_MAX_TIMEOUT = 3600
    DEF_WATER_MARK_FILE = "@chorkipro"

    BANNED_USERS = set(int(x) for x in os.environ.get("BANNED_USERS", "").split())

    DATABASE_URL = os.environ.get("DATABASE_URL", "mongodb+srv://himu1122:himu1122@cluster0.zfigslq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002775842088"))
    LOGGER = logging
    OWNER_ID = int(os.environ.get("OWNER_ID", "1700797877"))
    SESSION_NAME = "UploaderSKBot"
    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "-1002091196112")

    TG_MIN_FILE_SIZE = 2194304000
    BOT_USERNAME = os.environ.get("BOT_USERNAME", "trnuminfobot")
    ADL_BOT_RQ = {}

    # Set False off else True
    TRUE_OR_FALSE = os.environ.get("TRUE_OR_FALSE", "").lower() == "false"

    # Shortlink settings
    SHORT_DOMAIN = environ.get("SHORT_DOMAIN", "")
    SHORT_API = environ.get("SHORT_API", "")

    # Verification video link
    VERIFICATION = os.environ.get("VERIFICATION", "")

    
