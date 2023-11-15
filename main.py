import threading
from bot.bot import bot
from web.app import app
from shared.config import DISCORD_TOKEN
import logging

# Use the below to enable debug logging
# logger = logging.getLogger('nextcord')
# logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler()
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


def run():
    app.run(port=9999)


if __name__ == '__main__':
    # Start the Flask server in a new thread
    threading.Thread(target=run).start()

    bot.load_extension('slash_utilities')
    # Start the bot
    bot.run(DISCORD_TOKEN)
