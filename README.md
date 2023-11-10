
# Kernel Discord Bot

## Description

Kernel is a Discord bot integrated with a web server, capable of responding to webhooks and updating messages on Discord. It leverages Flask for the web server and Nextcord for Discord bot functionality.

## Features

- Web server running with Flask to handle webhook events.
- Discord bot capable of sending messages and responding to commands.
- Integration of Discord bot and web server in a multithreaded environment.
- Uses environment variables for configuration, enhancing security and flexibility.
- Containerized with Docker for easy deployment and scalability.

## Setup and Installation

### Prerequisites

- Python 3.9 or higher
- Docker and Docker Compose
- A Discord Bot Token

### Local Development

1. Clone the repository to your local machine.
2. Install the required Python dependencies:

\```sh
pip install -r requirements.txt
\```

3. Create a `.env` file at the root of the project with the following contents:

\```env
DISCORD_TOKEN=your_discord_bot_token
PREFIX=your_command_prefix
\```

4. Run the bot and web server:

\```sh
python main.py
\```

### Containerization with Docker

1. Ensure Docker and Docker Compose are installed on your system.
2. Build the Docker image:

\```sh
docker-compose build
\```

3. Start the service with Docker Compose:

\```sh
docker-compose up
\```

This will start the bot and web server within a Docker container named "Kernel".

## Usage

### Discord Commands

- `!hello`: The bot will reply with "Hello World!" in the Discord channel.

### Webhooks

- `/webhook`: Endpoint for receiving webhook events and updating Discord messages.
- `/update`: Endpoint for updating a message on Discord with the provided content.

## Deployment

The bot can be deployed to any environment that supports Docker. Use the provided `docker-compose.yml` file to build and run the container.

## Contributing

Contributions to Kernel are welcome! Please submit a pull request or open an issue if you have any features or improvements.

## License

N/A