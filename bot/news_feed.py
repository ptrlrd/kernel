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

    def load_latest_titles(self):
        if os.path.exists(self.latest_titles_file):
            with open(self.latest_titles_file, "r") as file:
                return json.load(file)
        return {}

    def save_latest_titles(self):
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

                # Determine the feed's title
                feed_title = feed.feed.title if 'title' in feed.feed else 'Unknown Feed'

                # Apply filtering logic based on feed title
                if "Hacker News" in feed_title:
                    should_post = True
                elif "Ars Technica" in feed_title:
                    if 'category' in entry:
                        categories = entry.category if isinstance(entry.category, list) else [entry.category]
                        should_post = 'Tech' in categories

                if should_post:
                    post_title = entry.get('title', 'No Title')
                    link = entry.get('link', '')
                    description = strip_tags(entry.get('summary', 'No Description'))
                    pub_date = entry.get('published', '')

                    # Combine feed title with post title
                    combined_title = f"{feed_title} - {post_title}"

                    if url not in self.latest_titles or self.latest_titles[url] != combined_title:
                        self.latest_titles[url] = combined_title
                        self.save_latest_titles()

                        embed = nextcord.Embed(
                            title=combined_title,
                            url=link,
                            description=description,
                            timestamp=datetime.datetime.now()
                        )
                        embed.set_footer(text=f"Published on {pub_date}")

                        await channel.send(embed=embed)

    @check_feeds.before_loop
    async def before_check_feeds(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(RSSFeedCog(bot))
