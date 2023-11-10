import threading
from bot.bot import bot
from web.app import app
from shared.config import DISCORD_TOKEN


def run():
    app.run(port=9999)


if __name__ == '__main__':
    # Start the Flask server in a new thread
    t = threading.Thread(target=run)
    t.start()

    # Start the bot
    bot.run(DISCORD_TOKEN)  # Replace 'YOUR TOKEN HERE' with your actual token
