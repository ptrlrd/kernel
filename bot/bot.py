import nextcord
from nextcord.ext import commands
from shared.config import CHANNEL_ID, DISCORD_TOKEN, GUILD_ID

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
    print('Bot is ready.')

# Importing slash commands and context menus
# from . import slash_commands, context_menus

if __name__ == '__main__':
    # Run the bot with the specified token
    bot.run(DISCORD_TOKEN)
