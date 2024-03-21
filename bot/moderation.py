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
        filepath = '/usr/src/app/data/banned_users.json'  # Adjusted path
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)  # Ensure directory exists
            with open(filepath, 'w') as file:
                json.dump([], file)
        with open(filepath, 'r') as file:
            return json.load(file)

    def save_banned_users(self, data):
        """Saves updated list of banned user patterns to the JSON file."""
        filepath = '/usr/src/app/data/banned_users.json'  # Adjusted path
        with open(filepath, 'w') as file:
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

    @bot.slash_command(name="remove_ban_pattern", description="Remove a username pattern from the ban list.")
    @commands.has_any_role(*STAFF_ROLES)
    async def remove_ban_pattern(self, interaction: nextcord.Interaction, pattern: str):
        """Removes a username pattern from the banned list."""
        banned_users = self.get_banned_users()
        if pattern in banned_users:
            banned_users.remove(pattern)
            self.save_banned_users(banned_users)
            await interaction.response.send_message(f"Pattern `{pattern}` removed from banned list.", ephemeral=True)
        else:
            await interaction.response.send_message(f"Pattern `{pattern}` is not in the banned list.", ephemeral=True)

    @bot.slash_command(name="list_ban_patterns", description="List all username patterns in the ban list.")
    @commands.has_any_role(*STAFF_ROLES)
    async def list_ban_patterns(self, interaction: nextcord.Interaction):
        """Lists all username patterns in the banned list."""
        banned_users = self.get_banned_users()
        if banned_users:
            patterns = "\n".join(banned_users)
            await interaction.response.send_message(f"Current banned patterns:\n```\n{patterns}\n```", ephemeral=True)
        else:
            await interaction.response.send_message("There are no patterns in the banned list.", ephemeral=True)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # This regex matches usernames with letters followed by an underscore and digits
        pattern = re.compile(r'^[a-zA-Z]+_\d+$')
        if pattern.match(member.name):
            channel = self.bot.get_channel(1105538041021472900)  # Make sure the ID is correct
            view = BanConfirmationView(member.name.split('_')[0] + '_\d+')  # Note the pattern change here for display purposes

            # Send the confirmation message with buttons
            message_text = f"Would you like to add the pattern for `{member.name.split('_')[0]}` followed by any number of digits to the bot ban list?"
            message = await channel.send(message_text, view=view)

            # Wait for the View to stop listening for interaction
            await view.wait()
            if view.value is True:
                # Add pattern to ban list and update JSON if confirmed
                banned_users = self.get_banned_users()
                new_pattern = member.name.split('_')[0] + '_\\d+'  # This is how you represent the pattern in the list
                if new_pattern not in banned_users:
                    banned_users.append(new_pattern)
                    self.save_banned_users(banned_users)
                    await message.edit(content=f"Pattern `{new_pattern}` added to banned list.", view=None)
                else:
                    await message.edit(content=f"Pattern `{new_pattern}` is already in the banned list.", view=None)
            elif view.value is False:
                # If declined, update the message
                await message.edit(content="Pattern addition cancelled.", view=None)


    @tasks.loop(hours=12)
    async def routine_check(self, interaction: nextcord.Interaction):
        """Performs a daily check on all server members against the banned username patterns."""
        banned_users = self.get_banned_users()
        for member in interaction.guild.members:
            for pattern in banned_users:
                if re.match(pattern, member.name):
                    await member.ban(reason="Routine check: Matched banned pattern.")
                    break

    @bot.slash_command(name="force_bot_check", description="Performs an immediate check of all members against the ban list.")
    @commands.has_any_role(*STAFF_ROLES)
    async def force_check(self, interaction: nextcord.Interaction):
        """Performs an immediate check against all members for banned username patterns."""
        await interaction.response.defer(ephemeral=True)  # Acknowledge the command interaction
        banned_users = self.get_banned_users()
        count = 0
        for member in interaction.guild.members:
            for pattern in banned_users:
                if re.match(pattern, member.name):
                    await member.ban(reason="Ad-hoc check: Matched banned pattern.")
                    count += 1
                    break  # Break to avoid multiple checks if multiple patterns match
        await interaction.followup.send(f"Ad-hoc check completed. Banned {count} user(s) matching the patterns.", ephemeral=True)

class BanConfirmationView(nextcord.ui.View):
    def __init__(self, pattern, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pattern = pattern
        self.value = None  # To track the staff's decision

@nextcord.ui.button(label='Yes', style=nextcord.ButtonStyle.green, emoji='👍')
async def confirm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    self.value = True
    self.stop()

@nextcord.ui.button(label='No', style=nextcord.ButtonStyle.red, emoji='👎')
async def cancel(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
    self.value = False
    self.stop()

def setup(bot):
    bot.add_cog(ModerationCog(bot))
