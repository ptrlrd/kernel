from dotenv import load_dotenv
import os

GUILD_ID = 930170875049820181
CHANNEL_ID = 978644045519802378  # This will be imported in both bot and web modules
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('PREFIX')
EMPLOYMENT_CHANNEL_ID = 1149747335442739300
SHOWCASE_CHANNEL_ID = 1137853999031263293
HELP_FORUM_CHANNEL_ID = 1105521800814801037
STAFF_ROLES = ["senior sudo", "sudo", "root", 99656376954916864, 931176500252782592, 1134275955431571486]
NEWS_CHANNEL_ID = 1193404886226845816
ERROR_LOG_CHANNEL_ID = 1175503125864513546
ENABLE_LOGGING = False  # Switch to True to enable logging
TESTING_MODE = False
RSS_FEED_URLS = ["https://hnrss.org/frontpage",
                 "https://www.databreaches.net/feed",
                 "https://feeds.arstechnica.com/arstechnica/technology-lab",
                 "https://www.wired.com/feed/rss",
                 ]

