import threading
from bot.bot import bot
from web.app import app
from shared.config import DISCORD_TOKEN, ENABLE_LOGGING
from shared.logger import setup_logging  # Importing from your logger module


def run():
    app.run(port=9999)


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
    # Start the bot
    bot.start_prometheus_server()
    bot.run(DISCORD_TOKEN)
