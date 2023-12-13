import requests
from nextcord import Interaction, ui, ButtonStyle, SlashOption, Member, Embed
from nextcord.ext import commands
from nextcord.ui import Button, View, ButtonStyle

from bot.bot import bot, update_message
from shared.config import STAFF_ROLES


class CoreCommandCogs(commands.Cog):
    """
    Cog for server interaction commands.
    """

    def __init__(self, bot, update_message_func):
        self.bot = bot
        self.update_message = update_message_func

    @bot.slash_command(name="hello", description="Says hello")
    async def hello(self, interaction: Interaction):
        await interaction.response.send_message("Hello World!", ephemeral=True)

    @bot.slash_command(name="vote", description="Vote for the server on different platforms!")
    async def vote(self, interaction: Interaction):
        view = ui.View()
        # Add voting platform buttons to the view
        view.add_item(ui.Button(style=ButtonStyle.url, label="Top.gg", url="https://top.gg/servers/930170875049820181"
                                                                           "#reviews"))
        view.add_item(ui.Button(style=ButtonStyle.url, label="Disboard", url="https://disboard.org/server"
                                                                             "/930170875049820181"))
        view.add_item(ui.Button(style=ButtonStyle.url, label="Discords", url="https://discords.com/servers/dev"))
        await interaction.response.send_message("Please vote for us!", view=view, ephemeral=True)

    @bot.slash_command(name="update_resources", description="Updates the message in #resources.")
    @commands.has_any_role(*STAFF_ROLES)
    async def update_command(self, interaction: Interaction):
        await interaction.response.defer(ephemeral=True)
        response = requests.get('https://raw.githubusercontent.com/ptrlrd/dpc-resources/main/resources.txt')
        content = response.text
        await self.update_message(content)
        await interaction.followup.send("Resources updated successfully!", ephemeral=True)


class UtilityCog(commands.Cog):
    """
    A utility cog for the bot, providing basic utility commands.

    This cog includes commands like ping, echo, and userinfo which serve
    as utility functions for users interacting with the bot.
    """

    def __init__(self, bot):
        """
        Initialize the UtilityCog with a reference to the bot.

        Args:
        bot: The instance of the bot that the cog is being added to.
        """
        self.bot = bot

    @bot.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: Interaction):
        """
        A slash command to check the bot's current latency.

        Args:
        interaction (Interaction): The interaction that triggered the command.
        """
        await interaction.response.send_message(f"Pong! Latency: {round(self.bot.latency * 1000)}ms")

    @bot.slash_command(name="echo", description="Repeat a message")
    async def echo(self, interaction: Interaction, message: str = SlashOption(description="The message to repeat")):
        """
        A slash command to repeat a message sent by the user.

        Args:
        interaction (Interaction): The interaction that triggered the command.
        message (str): The message to be repeated.
        """
        await interaction.response.send_message(message)

    @bot.slash_command(name="userinfo", description="Get information about a user")
    async def userinfo(self, interaction: Interaction,
                       user: Member = SlashOption(description="The user to get info about")):
        """
        A slash command to display information about a Discord user.

        Args:
        interaction (Interaction): The interaction that triggered the command.
        user (Member): The Discord member whose information is to be displayed.
        """
        embed = Embed(title="User Information", color=0x00ff00)
        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Joined at", value=user.joined_at, inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)

    @bot.slash_command(name="roadmap", description="Learn more about DevOps Roadmap")
    async def devops_roadmap(self, interaction: Interaction):
        embeds = [
            # ... (your roadmap embeds here)
        ]
        view = RoadmapEmbedView(embeds)
        await interaction.response.send_message(embed=embeds[0], view=view, ephemeral=True)


class RoadmapEmbedView(View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current = 0
        self.add_item(Button(label="Back to Beginning", style=ButtonStyle.grey))
        self.add_item(Button(label="Previous", style=ButtonStyle.blurple, disabled=True))
        self.add_item(Button(label="Next", style=ButtonStyle.blurple))

    @bot.ui.button(label="Back to Beginning", style=ButtonStyle.grey)
    async def back_to_beginning_button(self, button: Button, interaction: Interaction):
        self.current = 0
        self.children[1].disabled = True
        self.children[2].disabled = False
        await interaction.response.edit_message(embed=self.embeds[0], view=self)

    @bot.ui.button(label="Previous", style=ButtonStyle.blurple, disabled=True)
    async def previous_button(self, button: Button, interaction: Interaction):
        if self.current > 0:
            self.current -= 1
            await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
            self.children[2].disabled = False
        self.children[1].disabled = self.current == 0

    @bot.ui.button(label="Next", style=ButtonStyle.blurple)
    async def next_button(self, button: Button, interaction: Interaction):
        if self.current < len(self.embeds) - 1:
            self.current += 1
            await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
            self.children[1].disabled = False
        self.children[2].disabled = self.current == len(self.embeds) - 1


def setup(bot):
    """
    Setup function to add this cog to a bot.

    Args:
    bot: The bot instance to which the cog is being added.
    """
    bot.add_cog(CoreCommandCogs(bot, update_message))
    bot.add_cog(UtilityCog(bot))
