import nextcord
from nextcord.ext import tasks, commands
import feedparser
import datetime
from shared.config import NEWS_CHANNEL_ID, RSS_FEED_URLS
from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = []

    def handle_data(self, d):
        self.text.append(d)

    def get_data(self):
        return ''.join(self.text)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


class RSSFeedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feed_urls = RSS_FEED_URLS
        self.latest_titles_file = "latest_titles.json"  # JSON file for persistence
        self.latest_titles = self.load_latest_titles()
        self.channel_id = NEWS_CHANNEL_ID
        self.check_feeds.start()

    def load_latest_titles(self):
        if os.path.exists(self.latest_titles_file):
            with open(self.latest_titles_file, "r") as file:
                return json.load(file)
        return {}

    def save_latest_titles(self):
        with open(self.latest_titles_file, "w") as file:
            json.dump(self.latest_titles, file, indent=4)

    def load_latest_urls(self):
        if os.path.exists(self.latest_titles_file):
            with open(self.latest_titles_file, "r") as file:
                return json.load(file)
        return {}

    def save_latest_urls(self):
        with open(self.latest_titles_file, "w") as file:
            json.dump(self.latest_titles, file, indent=4)

    class RSSFeedCog(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            self.feed_urls = RSS_FEED_URLS
            self.channel_id = NEWS_CHANNEL_ID
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
                    if (current_time - published).total_seconds() < 60:  # Check if published in the last minute
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