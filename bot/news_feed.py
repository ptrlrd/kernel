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
        self.time_window = 60  # Time window in seconds
        self.channel = None
        self.check_feeds.start()

    async def get_channel(self):
        if not self.channel:
            self.channel = self.bot.get_channel(self.channel_id)
        return self.channel

    @tasks.loop(minutes=1)
    async def check_feeds(self):
        print("Checking feeds...")  # Debug print
        channel = await self.get_channel()
        if channel is None:
            print("Channel not found!")  # Debug print
            return

        current_time = datetime.datetime.now(datetime.timezone.utc)

        for url in self.feed_urls:
            try:
                feed = feedparser.parse(url)
                if feed.bozo:
                    print(f"Error parsing feed: {url}")  # Debug print
                    continue

                for entry in feed.entries:
                    published = datetime.datetime(*entry.published_parsed[:6], tzinfo=datetime.timezone.utc)
                    if (current_time - published).total_seconds() < self.time_window:
                        feed_title = feed.feed.title if 'title' in feed.feed else 'Unknown Feed'
                        link = entry.get('link', '')
                        message_text = f"Posting from *{feed_title}* : {link}"
                        print(f"Sending message: {message_text}")  # Debug print
                        await channel.send(message_text)
                        # ... Reaction adding code ...
            except Exception as e:
                print(f"An error occurred: {e}")  # Debug print

    @check_feeds.before_loop
    async def before_check_feeds(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(RSSFeedCog(bot))
