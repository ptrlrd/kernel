import nextcord
from nextcord.ext import tasks, commands
import feedparser
import datetime
from shared.config import NEWS_CHANNEL_ID, RSS_FEED_URLS

class RSSFeedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feed_urls = RSS_FEED_URLS
        self.channel_id = NEWS_CHANNEL_ID
        self.time_window = 360  # Time window in seconds to consider a publication as new
        self.check_feeds.start()

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
