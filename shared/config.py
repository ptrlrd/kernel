from dotenv import load_dotenv
import os

GUILD_ID = 930170875049820181
CHANNEL_ID = 978644045519802378  # This will be imported in both bot and web modules
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')