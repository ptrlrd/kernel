
# Kernel -- A Discord Bot
Used in the Devops, Programming, and Coding Discord
Join our discord here: https://discord.gg/devops-programming-and-cloud-930170875049820181

## Project Overview

This Discord bot, developed using Nextcord.py, is designed to enhance server functionality and user interaction on Discord. It includes features like command handling, context menus, and slash commands. The project is structured in a modular fashion and is deployed using Docker.

## Files and Directories

### Tree Structure
```
.
├── main.py
├── requirements.txt
├── Dockerfile
├── README.md
├── docker-compose.yaml
├── bot
│   ├── __init__.py
│   ├── bot.py
│   ├── context_menus.py
│   ├── slash_commands.py
│   └── utils.py
├── docker-compose.yaml
├── main.py
├── requirements.txt
├── shared
│   ├── __init__.py
│   └── config.py
└── web
    ├── __init__.py
    └── app.py
```

### Files

1. **bot.py**:
   - Main file of the bot, handling initialization and core functions.

2. **context_menus.py**:
   - Implements context menu commands for message interactions.

3. **slash_commands.py**:
   - Contains slash commands for user-friendly bot interactions.

4. **config.py**:
   - Manages configuration settings like tokens and channel IDs.

5. **app.py**:
   - Flask application to handle webhooks and update messages on Discord.

6. **main.py**:
   - Entry point for starting both the Discord bot and Flask server.

7. **Dockerfile**:
   - Instructions for Docker to build the bot's container.

8. **docker-compose.yaml**:
   - Configures the bot's service, using Docker Compose.

## Setup and Installation

### Prerequisites
- Python 3.9
- Docker (for containerized deployment)

### Local Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment variables in `.env`.
3. Run the bot: `python main.py`

### Docker Setup
1. Build and start the container: `sudo docker compose up --build -d `

## Usage

- The bot can be interacted with using slash commands or context menus in Discord.
- It responds to webhooks via the Flask server.

## Contributing

Contributions are welcome. Please adhere to the project's standards and submit pull requests for any changes.

## License

Review the License file for more information
