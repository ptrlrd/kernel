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
    if await has_required_role(interaction):
        message_link = f"https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
        notification = f"{message.author.mention}, please post your message in <#{channel_id}>. This channel is not for this type of conversation."

        # Send a reply to the original message
        await message.reply(notification)

        # Wait for 1 minutes
        await asyncio.sleep(60)
        try:
            await message.delete()
        except nextcord.NotFound:
            pass
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)


@bot.message_command(name="Send to employment")
async def send_to_show_case(interaction: Interaction, message: Message):
    await handle_command(interaction, message, EMPLOYMENT_CHANNEL_ID)


@bot.message_command(name="Send to show-case")
async def send_to_employment(interaction: Interaction, message: Message):
    await handle_command(interaction, message, SHOWCASE_CHANNEL_ID)


@bot.message_command(name="Send to help-forum")
async def send_to_help_forum(interaction: Interaction, message: Message):
    await handle_command(interaction, message, HELP_FORUM_CHANNEL_ID)
