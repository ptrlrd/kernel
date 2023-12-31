import asyncio

import nextcord
from nextcord import Message, Interaction
from nextcord.ext import commands

from bot.bot import bot
from shared.config import EMPLOYMENT_CHANNEL_ID, SHOWCASE_CHANNEL_ID, HELP_FORUM_CHANNEL_ID, STAFF_ROLES


class MessageManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def has_required_role(self, interaction: Interaction):
        """
        Check if the user in an interaction has one of the required roles.

        Args:
            interaction (Interaction): The Discord interaction object.

        Returns:
            bool: True if the user has one of the required roles, False otherwise.
        """
        if isinstance(interaction.user, nextcord.Member):
            return any(role.name in STAFF_ROLES for role in interaction.user.roles)
        return False

    async def handle_command(self, interaction: Interaction, message: Message, channel_id: int):
        """
        Handle the command to move a message to a specified channel.

        Args:
            interaction (Interaction): The interaction that triggered the command.
            message (Message): The message to be moved.
            channel_id (int): The ID of the channel to move the message to.

        This function checks if the user has the required role, sends a notification
        to the message author, and then deletes the original message after a countdown.
        """
        # Acknowledge the interaction immediately
        await interaction.response.defer(ephemeral=True)

        if await self.has_required_role(interaction):
            notification = f"{message.author.mention}, please post your message in <#{channel_id}>. This channel is not for this type of conversation."
            await message.reply(notification)

            countdown_duration = 60
            countdown_message = await interaction.followup.send(
                f"Message will be deleted in {countdown_duration} seconds.", ephemeral=True)

            while countdown_duration > 0:
                await asyncio.sleep(5)
                countdown_duration -= 5
                await countdown_message.edit(content=f"Message will be deleted in {countdown_duration} seconds.")

            try:
                await message.delete()
                await countdown_message.edit(content="Message has been deleted.")
            except nextcord.NotFound:
                pass
        else:
            await interaction.followup.send("You do not have permission to use this command.", ephemeral=True)

    @bot.message_command(name="Send to employment")
    async def send_to_employment(self, interaction: Interaction, message: Message):
        """
        Discord message command to send a message to the employment channel.

        Args:
            interaction (Interaction): The interaction that triggered the command.
            message (Message): The message to be moved.
        """
        await self.handle_command(interaction, message, EMPLOYMENT_CHANNEL_ID)

    @bot.message_command(name="Send to show-case")
    async def send_to_show_case(self, interaction: Interaction, message: Message):
        """
        Discord message command to send a message to the showcase channel.

        Args:
            interaction (Interaction): The interaction that triggered the command.
            message (Message): The message to be moved.
        """
        await self.handle_command(interaction, message, SHOWCASE_CHANNEL_ID)

    @bot.message_command(name="Send to help-forum")
    async def send_to_help_forum(self, interaction: Interaction, message: Message):
        """
        Discord message command to send a message to the help forum channel.

        Args:
            interaction (Interaction): The interaction that triggered the command.
            message (Message): The message to be moved.
        """
        await self.handle_command(interaction, message, HELP_FORUM_CHANNEL_ID)

    @bot.message_command(name="Use the /roadmap command")
    async def use_roadmap_command(self, interaction: Interaction, message: Message):
        """
        Discord message command to instruct users to use the /roadmap slash command.

        Args:
            interaction (Interaction): The interaction that triggered the command.
            message (Message): The message where the command was invoked.
        """
        await interaction.response.send_message("Please use the `/roadmap` slash command to view the DevOps Roadmap.")


def setup(bot):
    bot.add_cog(MessageManagementCog(bot))
