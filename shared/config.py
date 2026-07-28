import os
from dotenv import load_dotenv
load_dotenv()

class Settings:
    MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1-8b-instant")
    HF_TOKEN = os.getenv("HF_TOKEN")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

settings = Settings()