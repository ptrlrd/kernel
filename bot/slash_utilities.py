from nextcord import Interaction, SlashOption, Member, Embed
from nextcord.ext import commands

from bot.bot import bot

#TODO: Merge Slash_Utility.py and Slash_Commands.py into one file and delete this one and use cogs


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
    async def userinfo(self, interaction: Interaction, user: Member = SlashOption(description="The user to get info about")):
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


def setup(bot):
    """
    Setup function to add this cog to a bot.

    Args:
    bot: The bot instance to which the cog is being added.
    """
    bot.add_cog(UtilityCog(bot))
