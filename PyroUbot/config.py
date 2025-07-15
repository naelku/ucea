import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

DEVS = list(map(int, os.getenv("DEVS", "1577255151").split()))

API_ID = int(os.getenv("API_ID", "25027112"))

API_HASH = os.getenv("API_HASH", "2121832cdd238e3bc78037ca8a2723fd")

BOT_TOKEN = os.getenv("BOT_TOKEN", "7675884004:AAEdOrcg0IhUJPrBeb8IB_PA1sRqpbFDfDE")

OWNER_ID = int(os.getenv("OWNER_ID", "1577255151"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002125842026 -1002053287763").split()))

RMBG_API = os.getenv("RMBG_API", "a6qxsmMJ3CsNo7HyxuKGsP1o")

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://aortulsk:KxCX5EQdssavL4dm@cluster0.qsywpr2.mongodb.net/")

LOGS_MAKER_UBOT = int(os.getenv("LOGS_MAKER_UBOT", "-4912568273"))
