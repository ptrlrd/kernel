from nextcord import Interaction, SlashOption
from nextcord.ext import commands

from bot.bot import bot


class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong! Latency: {round(self.bot.latency * 1000)}ms")

    @bot.slash_command(name="echo", description="Repeat a message")
    async def echo(self, interaction: Interaction, message: str = SlashOption(description="The message to repeat")):
        await interaction.response.send_message(message)

    @bot.slash_command(name="userinfo", description="Get information about a user")
    async def userinfo(self, interaction: Interaction,
                       user: bot.Member = SlashOption(description="The user to get info about")):
        embed = bot.Embed(title="User Information", color=0x00ff00)
        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(name="ID", value=user.id, inline=False)
        embed.add_field(name="Joined at", value=user.joined_at, inline=False)
        embed.set_thumbnail(url=user.avatar.url)
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(UtilityCog(bot))