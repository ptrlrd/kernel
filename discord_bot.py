from discord.ext import commands
from flask import Flask, request
import discord
import threading
import requests
import json

app = Flask(__name__)
CHANNEL_ID = 978644045519802378

# Start the bot
intents = discord.Intents.all()
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
    # Clear the channel
    await clear_channel(channel)

    # Split the content and send separate messages
    sections = content.split("## ")
    for section in sections:
        # Ensure section is not empty or just whitespace
        if section and not section.isspace():
            await channel.send(f"## {section}")

@app.route('/webhook', methods=['POST'])
def respond():
    print("Received a webhook event")
    data = request.get_json()

    # Github information extraction
    github_user = data['sender']['login']
    commit_hash = data['after']
    github_commit_url = data['repository']['html_url'] + "/commit/" + commit_hash

    # Get the file content
    r = requests.get('https://raw.githubusercontent.com/ptrlrd/dpc-resources/main/resources.txt')
    content = r.text

    # Update the message on Discord
    bot.loop.create_task(update_message(content))
    return "", 200

@app.route('/update', methods=['POST'])
def update():
    content = request.json['content']
    bot.loop.create_task(update_message(content))
    return "", 200

def run():
    app.run(port=9999)

# Start the Flask server in a new thread
t = threading.Thread(target=run)
t.start()

bot.run('REDACTED')
