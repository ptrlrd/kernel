from nextcord.ext import commands, tasks
import nextcord
import json
import os
import re
from bot.bot import bot
from shared.config import STAFF_ROLES

class ModerationCog(commands.Cog):
    """
    A cog dedicated to moderation tasks, including banning users based on username patterns.
    """

    def __init__(self, bot):
        self.bot = bot

    def get_banned_users(self):
        """Checks for the existence of the banned_users.json file or creates it."""
        if not os.path.exists('banned_users.json'):
            with open('banned_users.json', 'w') as file:
                json.dump([], file)
        with open('banned_users.json', 'r') as file:
            return json.load(file)

    def save_banned_users(self, data):
        """Saves updated list of banned user patterns to the JSON file."""
        with open('banned_users.json', 'w') as file:
            json.dump(data, file)

    @bot.slash_command(name="add_ban_pattern", description="Add a username pattern to ban list.")
    @commands.has_any_role(*STAFF_ROLES)
    async def add_ban_pattern(self, interaction: nextcord.Interaction, pattern: str):
        """Adds a new username pattern to the banned list."""
        banned_users = self.get_banned_users()
        if pattern not in banned_users:
            banned_users.append(pattern)
            self.save_banned_users(banned_users)
            await interaction.response.send_message(f"Pattern `{pattern}` added to banned list.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Pattern `{pattern}` is already in the banned list.", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Checks joining members against the banned username patterns and bans if matched."""
        banned_users = self.get_banned_users()
        for pattern in banned_users:
            if re.match(pattern, member.name):
                await member.ban(reason="Matched banned pattern.")
                break

    @tasks.loop(hours=24)
    async def routine_check(self):
        """Performs a daily check on all server members against the banned username patterns."""
        banned_users = self.get_banned_users()
        for guild in self.bot.guilds:
            for member in guild.members:
                for pattern in banned_users:
                    if re.match(pattern, member.name):
                        await member.ban(reason="Routine check: Matched banned pattern.")
                        break

def setup(bot):
    bot.add_cog(ModerationCog(bot))
