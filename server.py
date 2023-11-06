from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    if request.headers.get('X-GitHub-Event') == "push":
        file_url = 'https://raw.githubusercontent.com/ptrlrd/dpc-resources/main/resources.txt'
        response = requests.get(file_url)

        if response.status_code == 200:
            content = response.text
            with open('content.json', 'w') as f:
                json.dump({'content': content}, f)

            # Notify the Discord bot to update the message
            requests.post('http://discord_bot_url/update')

        else:
            print('Unable to fetch file contents')

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
