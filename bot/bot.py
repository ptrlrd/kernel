import nextcord
from nextcord.ext import commands
from shared.config import CHANNEL_ID, DISCORD_TOKEN, GUILD_ID, BOT_STATUS, BOT_NAME

# Create an instance of the bot with all intents enabled
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def clear_channel(channel):
    """
    Clears all messages from the given channel.

    Args:
    channel (nextcord.Channel): The Discord channel from which messages will be purged.
    """
    await channel.purge()

async def update_message(content):
    """
    Updates a message in a specific channel, splitting the content by sections.

    This function clears the channel first and then sends each section of the content
    as a separate message.

    Args:
    content (str): The content to be split and sent to the channel.
    """
    channel = bot.get_channel(CHANNEL_ID)
    await clear_channel(channel)

    sections = content.split("## ")
    for section in sections:
        if section and not section.isspace():
            await channel.send(f"## {section}")

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

