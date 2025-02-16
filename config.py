# config.py
from dotenv import load_dotenv
import os

# Carrega o arquivo .env do diretório atual
load_dotenv()

class Config:
    # Usamos .strip() para remover possíveis espaços ou quebras de linha
    USERNAME = (os.getenv("USERNAME") or "").strip()
    PASSWORD = (os.getenv("PASSWORD") or "").strip()
    OTP_SECRET = (os.getenv("OTP_SECRET") or "").strip()
