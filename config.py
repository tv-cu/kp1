from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
API_KEY = getenv("API_KEY", "JrraFpHWR88PBVYPmrWRvv3YnfVBfuY4")
REQUEST_TIMEOUT = getenv("REQUEST_TIMEOUT", 10)
