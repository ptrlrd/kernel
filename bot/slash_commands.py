import requests
from nextcord import Interaction, ui, ButtonStyle
from nextcord.ext import commands

from bot.bot import bot, update_message

STAFF_ROLES = ["Staff", "Senior Staff", "Root"]  # Replace with actual role names or IDs


@bot.slash_command(name="hello", description="Says hello")
async def hello(interaction: Interaction):
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

    await interaction.response.send_message("Please vote for us!", view=view, ephemeral=True)


@bot.slash_command(name="update_resources", description="Updates the message in #resources.")
@commands.has_any_role(*STAFF_ROLES)
async def update_command(interaction: Interaction):
    # Defer the response if the operation might take longer
    await interaction.response.defer(ephemeral=True)

    # Fetch the content and update the message
    response = requests.get('https://raw.githubusercontent.com/ptrlrd/dpc-resources/main/resources.txt')
    content = response.text
    await update_message(content)

    # Send a follow-up message
    await interaction.followup.send("Resources updated successfully!", ephemeral=True)