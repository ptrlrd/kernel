import nextcord
from nextcord.ext import commands
from shared.config import CHANNEL_ID, DISCORD_TOKEN, GUILD_ID

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

async def clear_channel(channel):
    await channel.purge()

async def update_message(content):
    channel = bot.get_channel(CHANNEL_ID)
    await clear_channel(channel)

    sections = content.split("## ")
    for section in sections:
        if section and not section.isspace():
            await channel.send(f"## {section}")

@bot.event
async def on_ready():
    print('Bot is ready.')

from . import slash_commands,context_menus

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
