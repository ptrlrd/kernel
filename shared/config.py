from dotenv import load_dotenv
import os

CHANNEL_ID = 978644045519802378  # This will be imported in both bot and web modules
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')