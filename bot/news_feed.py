import nextcord
from nextcord.ext import tasks, commands
from nextcord import Interaction, ButtonStyle
import feedparser
import json
import os
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

    def load_latest_urls(self):
        if os.path.exists(self.latest_titles_file):
            with open(self.latest_titles_file, "r") as file:
                return json.load(file)
        return {}

    def save_latest_urls(self):
        with open(self.latest_titles_file, "w") as file:
            json.dump(self.latest_titles, file, indent=4)

    @tasks.loop(minutes=1)
    async def check_feeds(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel is None:
            return

        for url in self.feed_urls:
            feed = feedparser.parse(url)

            for entry in feed.entries:
                should_post = False
                feed_title = feed.feed.title if 'title' in feed.feed else 'Unknown Feed'

                # Logic to determine whether to post the entry
                # ...

                link = entry.get('link', '')
                if link and (link not in self.latest_titles):
                    self.latest_titles[link] = True  # Mark this link as posted
                    self.save_latest_urls()

                    message_text = f"Posting from *{feed_title}* : [link]({link})"
                    message = await channel.send(message_text)

                    # Add reactions for thumbs up and thumbs down
                    await message.add_reaction("👍")
                    await message.add_reaction("👎")

    @check_feeds.before_loop
    async def before_check_feeds(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(RSSFeedCog(bot))
