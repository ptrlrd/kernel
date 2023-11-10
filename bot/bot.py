import nextcord
from shared.config import CHANNEL_ID, DISCORD_TOKEN, GUILD_ID
from nextcord.ext import commands
from nextcord import Interaction, ui, ButtonStyle

# Initialize the bot with the appropriate intents
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)


# Define the clear_channel function
async def clear_channel(channel):
    await channel.purge()


# Define the update_message function
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


# Define your slash commands and events below
list_of_guilds = [GUILD_ID]  # Replace with your actual guild IDs
bot.test_guilds = list_of_guilds  # Apply the list of test guilds to the bot instance


@bot.slash_command(name="hello", description="Says hello")
async def hello(interaction: nextcord.Interaction):
    await interaction.response.send_message("Hello World!", ephemeral=True)


@bot.slash_command(name="vote", description="Vote for the server on different platforms!")
async def vote(interaction: Interaction):
    # Create a view to hold our buttons
    view = ui.View()

    # Add buttons to the view
    view.add_item(
        ui.Button(style=ButtonStyle.url, label="Top.gg", url="https://top.gg/servers/930170875049820181#reviews"))
    view.add_item(
        ui.Button(style=ButtonStyle.url, label="Disboard", url="https://disboard.org/server/930170875049820181"))
    view.add_item(ui.Button(style=ButtonStyle.url, label="Discords", url="https://discords.com/servers/dev"))

    # Send the ephemeral message with the buttons
    await interaction.response.send_message("Please vote for us using the buttons below!", view=view, ephemeral=True)


@bot.event
async def on_ready():
    print('Bot is ready.')


# The main execution point
if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)
