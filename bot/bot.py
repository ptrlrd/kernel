from nextcord.ext import commands
import nextcord
from shared.config import CHANNEL_ID

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command()
async def hello(ctx):
    await ctx.send("Hello World!")


@bot.event
async def on_ready():
    print('Bot is ready.')


async def clear_channel(channel):
    await channel.purge()


async def update_message(content):
    channel = bot.get_channel(CHANNEL_ID)
    await clear_channel(channel)
    sections = content.split("## ")
    for section in sections:
        if section and not section.isspace():
            await channel.send(f"## {section}")
