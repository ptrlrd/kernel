from flask import Flask, request
import requests
from bot.bot import update_message, bot

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def respond():
    """
    Responds to webhook events.

    This route is triggered via a POST request to '/webhook'. It fetches content
    from a specified URL and creates a task to update a message with this content
    on Discord.

    Returns:
    A tuple containing an empty string and the HTTP status code 200.
    """
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
    """
    Updates the message on Discord with provided content.

    This route is triggered via a POST request to '/update'. It gets the content
    from the request's JSON body and creates a task to update a message with this
    content on Discord.

    Returns:
    A tuple containing an empty string and the HTTP status code 200.
    """
    content = request.json['content']
    bot.loop.create_task(update_message(content))
    return "", 200
