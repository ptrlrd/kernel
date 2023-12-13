import asyncio
import nextcord
from nextcord import Message, Interaction, ButtonStyle
from nextcord.ext import commands
from shared.config import EMPLOYMENT_CHANNEL_ID, SHOWCASE_CHANNEL_ID, HELP_FORUM_CHANNEL_ID, STAFF_ROLES
from nextcord.ui import Button, View
from bot.bot import bot


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

    @bot.message_command(name="Send Devops Roadmap")
    async def send_devops_roadmap(self, interaction: nextcord.Interaction, message: nextcord.Message):
        """
        Discord message command to send the DevOps Roadmap.

        Args:
            interaction (Interaction): The interaction that triggered the command.
            message (Message): The message where the command was invoked.
        """
        embeds = [
            nextcord.Embed(title="What is DevOps?",
                           description="DevOps is all about bringing developers and operations teams together to improve software delivery. The key focus areas are automation, infrastructure and monitoring."),
            nextcord.Embed(title="Learn a Programming Language",
                           description="Python, Go, Pick any Programming Language. You can pick any programming language. The purpose behind the language is to be able to write automation scripts to automate repetitive tasks."),
            nextcord.Embed(title="Linux",
                           description="Learn about the file system, package managers, managing services, checking logs, bash scripting, permissions, pipes output redirection, common tools for text manipulation process monitoring, networking tools, CLI editors etc. Pick Ubuntu if you have a little to no experience."),
            nextcord.Embed(title="Networking and Protocols",
                           description="Learn about DNS, TCP/IP Protocols, SSH, ports, gateways, routing, ip addressing, and subnetting etc. This will come in handy with deployments / troubleshooting."),
            nextcord.Embed(title="Docker",
                           description="Learn about containerization. Be comfortable writing Docker files. Learn about troubleshooting. Get familiar with Alpine Linux. Learn about networking, storage, security. Learn docker networking, storage, security, performance."),
            nextcord.Embed(title="Git",
                           description="DevOps teams usually practice 'git ops,' i.e., making changes to your CI/CD pipeline, infrastructure, or server provisioning will involve making a pull request against the appropriate git repository. Learn about git, create your GitHub profile."),
            nextcord.Embed(title="Learn the Cloud",
                           description="Pick one of the cloud providers AWS, GCP or Azure. Start with core services e.g. in AWS VPC, EC2, S3, IAM and later RDS, Route53, Cloudwatch, ECS, etc. Create and deploy some dummy application to the cloud."),
            nextcord.Embed(title="Terraform",
                           description="Learn what 'Infrastructure as Code' means. Learn about terraform and how to automate infrastructure creation. If you deployed an application to AWS in previous step destroy the infrastructure and create it using terraform."),
            nextcord.Embed(title="Ansible",
                           description="Learn what is configuration management. Understand roles, playbooks, inventory management and automation. Write some automation scripts e.g. db backups."),
            nextcord.Embed(title="GitHub Actions",
                           description="Learn about the concepts of CI/CD and how to implement in your projects using some CI/CD tool. There are several options available in this space, you can pick any one. Integrate CI/CD into your apps using GitHub Actions."),
            nextcord.Embed(title="Nginx",
                           description="nginx is commonly used for web serving, reverse proxying, caching, load balancing, media streaming, and more. Learn the basic config options, TLS setup etc."),
            nextcord.Embed(title="Job Ready",
                           description="At this point, you should have enough knowledge to find a junior to mid-level (maybe even senior) DevOps position at any company depending on the depth of your knowledge. Deepen your pool of knowledge and keep building projects till you find a job. Your job will teach you a lot as well. Continue learning at https://roadmap.sh/devops.")
        ]
        view = RoadmapEmbedView(embeds)
        await interaction.response.send_message(embed=embeds[0], view=view)


class RoadmapEmbedView(View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current = 0
        self.add_item(Button(style=ButtonStyle.grey, emoji="⬅️", custom_id="previous", disabled=True))
        self.add_item(Button(style=ButtonStyle.grey, emoji="➡️", custom_id="next"))

    @nextcord.ui.button(label="Previous", style=ButtonStyle.blurple, disabled=True)
    async def previous_button(self, button: Button, interaction: Interaction):
        if self.current > 0:
            self.current -= 1
            if self.current == 0:
                button.disabled = True
            await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
        self.children[1].disabled = False  # Enable the 'next' button

    @nextcord.ui.button(label="Next", style=ButtonStyle.blurple)
    async def next_button(self, button: Button, interaction: Interaction):
        if self.current < len(self.embeds) - 1:
            self.current += 1
            if self.current == len(self.embeds) - 1:
                button.disabled = True
            await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
        self.children[0].disabled = False  # Enable the 'previous' button


def setup(bot):
    bot.add_cog(MessageManagementCog(bot))
