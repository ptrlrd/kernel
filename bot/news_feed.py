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


class LinkButton(nextcord.ui.View):
    def __init__(self, url):
        super().__init__()
        self.add_item(nextcord.ui.Button(style=ButtonStyle.url, label="Link to Article", url=url))


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
            latest_entry = feed.entries[0] if feed.entries else None

            if latest_entry:
                title = latest_entry.get('title', 'No Title')
                link = latest_entry.get('link', '')
                description = strip_tags(latest_entry.get('summary', 'No Description'))
                pub_date = latest_entry.get('published', '')

                if url not in self.latest_titles or self.latest_titles[url] != title:
                    self.latest_titles[url] = title
                    self.save_latest_titles()

                    embed = nextcord.Embed(
                        title=title,
                        url=link,
                        description=description,
                        timestamp=datetime.datetime.now()
                    )
                    embed.set_footer(text=f"Published on {pub_date}")
                    view = LinkButton(link)

                    await channel.send(embed=embed, view=view)

    @check_feeds.before_loop
    async def before_check_feeds(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(RSSFeedCog(bot))
