import nextcord
from nextcord import Interaction, Message
from bot.bot import bot
import asyncio
from shared.config import EMPLOYMENT_CHANNEL_ID, SHOWCASE_CHANNEL_ID, HELP_FORUM_CHANNEL_ID

STAFF_ROLES = ["Staff", "Senior Staff", "Root"]  # Replace with actual role names or IDs


async def has_required_role(interaction: Interaction):
    if isinstance(interaction.user, nextcord.Member):
        return any(role.name in STAFF_ROLES for role in interaction.user.roles)
    return False


async def handle_command(interaction: Interaction, message: Message, channel_id: int):
    # Acknowledge the interaction immediately
    await interaction.response.defer(ephemeral=True)

    if await has_required_role(interaction):
        notification = f"{message.author.mention}, please post your message in <#{channel_id}>. This channel is not for this type of conversation."

        # Send a reply to the original message
        sent_notification = await message.reply(notification)

        # Countdown duration in seconds
        countdown_duration = 60

        # Send initial ephemeral countdown message
        countdown_message = await interaction.followup.send(f"Message will be deleted in {countdown_duration} seconds.", ephemeral=True)

        while countdown_duration > 0:
            await asyncio.sleep(5)  # Update the countdown every 5 seconds
            countdown_duration -= 5
            # Update the countdown message (ephemeral)
            await countdown_message.edit(content=f"Message will be deleted in {countdown_duration} seconds.")

        try:
            await message.delete()
            await sent_notification.delete()
            await countdown_message.edit(content="Message has been deleted.")
        except nextcord.NotFound:
            pass
    else:
        # Send a follow-up ephemeral message since we've already acknowledged the interaction
        await interaction.followup.send("You do not have permission to use this command.", ephemeral=True)


@bot.message_command(name="Send to employment")
async def send_to_show_case(interaction: Interaction, message: Message):
    await handle_command(interaction, message, EMPLOYMENT_CHANNEL_ID)


@bot.message_command(name="Send to show-case")
async def send_to_employment(interaction: Interaction, message: Message):
    await handle_command(interaction, message, SHOWCASE_CHANNEL_ID)


@bot.message_command(name="Send to help-forum")
async def send_to_help_forum(interaction: Interaction, message: Message):
    await handle_command(interaction, message, HELP_FORUM_CHANNEL_ID)
