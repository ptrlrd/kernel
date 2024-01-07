import nextcord
from nextcord.ext import tasks, commands
import feedparser
import datetime
from shared.config import NEWS_CHANNEL_ID, RSS_FEED_URLS, TESTING_MODE

class RSSFeedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feed_urls = RSS_FEED_URLS
        self.channel_id = NEWS_CHANNEL_ID
        self.time_window = 3600  # Time window in seconds
        self.posted_entries = set()  # Track posted entries
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
                entry_id = entry.get('id', entry.get('link', ''))

                if entry_id in self.posted_entries:
                    continue  # Skip already posted entries

                if TESTING_MODE:
                    pass
                else:
                    published = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
                    time_diff = (current_time - published).total_seconds()
                    if time_diff >= self.time_window:
                        continue

                feed_title = feed.feed.title if 'title' in feed.feed else 'Unknown Feed'
                link = entry.get('link', '')
                message_text = f"Posting from *{feed_title}* : {link}"
                try:
                    message = await channel.send(message_text)
                    await message.add_reaction("👍")
                    await message.add_reaction("👎")
                    self.posted_entries.add(entry_id)  # Mark as posted
                except Exception as e:
                    print(f"Error sending message: {e}")

    @check_feeds.before_loop
    async def before_check_feeds(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(RSSFeedCog(bot))
