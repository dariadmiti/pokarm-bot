import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
DASHA_ID = os.getenv('DASHA_ID')
DENIS_ID = os.getenv('DENIS_ID')
BOT_API_TOKEN = os.getenv('BOT_API_TOKEN')
