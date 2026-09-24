from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("DISCORD_TOKEN")
database_url = os.getenv("DATABASE_URL")

if not token:
    raise ValueError("discord token ausente")

class Config:

    TOKEN = token
    DATABASE_URL = database_url