import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DJANGO_API_URL = os.getenv(
    "DJANGO_API_URL", "http://127.0.0.1:8000/link-telegram/"
)
