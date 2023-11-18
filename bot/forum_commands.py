from bot.bot import bot
from shared.config import HELP_FORUM_CHANNEL_ID
from nextcord.ext import commands

# Global variable to toggle features
STAFF_ROLES = ["Staff", "Senior Staff", "Root"]  # Replace with actual role names or IDs

features_enabled = True

tracked_messages = {}


@bot.slash_command(name="togglefeatures", description="Toggle the forum tracking features on or off")
@commands.has_any_role(*STAFF_ROLES)  # Or use any other method to restrict access
async def toggle_features(interaction: bot.Interaction):
    global features_enabled
    features_enabled = not features_enabled
    status = "enabled" if features_enabled else "disabled"
    await interaction.response.send_message(f"Forum tracking features are now {status}.", ephemeral=True)


@bot.event
async def on_message(message):
    if not features_enabled:
        return
    if message.channel.id == HELP_FORUM_CHANNEL_ID:
        await message.reply(
            "Hey there! Thanks for posting your question, if someone answers the question right click the message > "
            "apps > Solved my Q")

        # Track the message
        tracked_messages[message.id] = {'author_id': message.author.id, 'solved': False}


@bot.event
async def on_interaction(interaction):
    if not features_enabled:
        return
    if interaction.type == bot.InteractionType.component:
        custom_id = interaction.component.custom_id

        if custom_id == 'solved_my_q':
            message_id = interaction.message.id

            if message_id in tracked_messages and interaction.user.id == tracked_messages[message_id]['author_id']:
                # Mark as solved
                tracked_messages[message_id]['solved'] = True
                await interaction.response.send_message("Your question has been marked as solved!", ephemeral=True)

                # Retrieve the original message (forum thread)
                original_message = await interaction.channel.fetch_message(message_id)

                # Apply the 'Solved' tag
                solved_tag = None
                for tag in original_message.channel.tags:
                    if tag.name.lower() == 'solved':
                        solved_tag = tag
                        break

                if solved_tag:
                    await original_message.edit(tags=[solved_tag])
                else:
                    await interaction.followup.send("The 'Solved' tag could not be found in this channel.",
                                                    ephemeral=True)

