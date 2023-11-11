from nextcord import Interaction, ui, ButtonStyle
from bot.bot import bot

@bot.slash_command(name="hello", description="Says hello")
async def hello(interaction: Interaction):
    await interaction.response.send_message("Hello World!", ephemeral=True)

@bot.slash_command(name="vote", description="Vote for the server on different platforms!")
async def vote(interaction: Interaction):
    # Create a view to hold our buttons
    view = ui.View()

    # Add buttons to the view
    view.add_item(ui.Button(style=ButtonStyle.url, label="Top.gg", url="https://top.gg/servers/930170875049820181#reviews"))
    view.add_item(ui.Button(style=ButtonStyle.url, label="Disboard", url="https://disboard.org/server/930170875049820181"))
    view.add_item(ui.Button(style=ButtonStyle.url, label="Discords", url="https://discords.com/servers/dev"))

    await interaction.response.send_message("Please vote for us!", view=view, ephemeral=True)
