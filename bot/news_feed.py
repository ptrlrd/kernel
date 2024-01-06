import logging
import asyncio
from nextcord.ext import tasks, commands
import feedparser
import datetime
from shared.config import NEWS_CHANNEL_ID, ERROR_LOG_CHANNEL_ID, RSS_FEED_URLS

class DiscordLoggingHandler(logging.Handler):
    def __init__(self, bot, channel_id):
        super().__init__()
        self.bot = bot
        self.channel_id = channel_id

    def emit(self, record):
        msg = self.format(record)
        asyncio.create_task(self.send_to_discord(msg))

    async def send_to_discord(self, msg):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(f"```\n{msg}\n```")

class RSSFeedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feed_urls = RSS_FEED_URLS
        self.channel_id = NEWS_CHANNEL_ID
        self.error_log_channel_id = ERROR_LOG_CHANNEL_ID
        self.time_window = 360
        self.check_feeds.start()
        self.setup_logging()

    def setup_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.ERROR)
        handler = DiscordLoggingHandler(self.bot, self.error_log_channel_id)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @tasks.loop(minutes=1)
    async def check_feeds(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            return

        current_time = datetime.datetime.now(datetime.timezone.utc)

        for url in self.feed_urls:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                published = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
                if (current_time - published).total_seconds() < self.time_window:
                    feed_title = feed.feed.title if 'title' in feed.feed else 'Unknown Feed'
                    link = entry.get('link', '')
                    message_text = f"Posting from *{feed_title}* : {link}"
                    message = await channel.send(message_text)

                    await message.add_reaction("👍")
                    await message.add_reaction("👎")

    @check_feeds.before_loop
    async def before_check_feeds(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(RSSFeedCog(bot))
