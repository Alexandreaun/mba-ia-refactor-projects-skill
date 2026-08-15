import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    DB_PATH = os.environ.get("DB_PATH", "loja.db")
    PORT = int(os.environ.get("PORT", "5050"))
