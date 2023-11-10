from flask import Flask, request
import requests
from bot.bot import update_message, bot

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def respond():
    print("Received a webhook event")
    data = request.get_json()

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
