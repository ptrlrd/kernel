import threading
import asyncio
from bot.bot import bot
from web.app import app
from shared.config import DISCORD_TOKEN, ENABLE_LOGGING, BOT_STATUS, BOT_NAME
from shared.logger import setup_logging  # Importing from your logger module
from prometheus_client import start_http_server
import time


async def start_bot():
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        try:
            await bot.start(DISCORD_TOKEN)
        except aiohttp.client_exceptions.ClientConnectorError as e:
            print(f"Connection error: {e}. Retrying in 10 seconds...")
            retry_count += 1
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

def start_prometheus_server():
    # Start a Prometheus HTTP server on port 8000
    start_http_server(8000, addr='0.0.0.0')
    print("Prometheus server started on port 8000")

def run():
    app.run(port=9999)

@bot.event
async def on_ready():
    """
    An event listener for when the bot is ready and operational.

    Prints a message to the console to indicate that the bot is ready.
    """
    print(f'{BOT_NAME} has connected to Discord!')
    # Mark the bot as "up" when it is online
    BOT_STATUS.labels(bot_name=BOT_NAME).set(1)


@bot.event
async def on_disconnect():
    print(f'{BOT_NAME} has disconnected from Discord!')
    # Mark the bot as "down" when it is offline
    BOT_STATUS.labels(bot_name=BOT_NAME).set(0)

if __name__ == '__main__':
    if ENABLE_LOGGING:
        setup_logging()  # Setup logging using the function from shared.logger
        # To enable extensive logging go to /shared/config.py and set ENABLE_LOGGING to True

    # Start the Flask server in a new thread
    threading.Thread(target=run).start()
    # Load the slash commands and context menus
    bot.load_extension('bot.slash_commands')
    bot.load_extension('bot.context_menus')
    bot.load_extension('bot.news_feed')
    # bot.load_extension('bot.moderation') Turning off because it's not working
    start_prometheus_server()
    asyncio.run(start_bot())
