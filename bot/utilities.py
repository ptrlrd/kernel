import sqlite3
from nextcord.ext import commands

class MessageManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('user_messages.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS UserMessages
                            (UserID TEXT PRIMARY KEY, MessageCount INTEGER)''')

    async def on_message(self, message):
        user_id = str(message.author.id)
        self.cursor.execute("SELECT MessageCount FROM UserMessages WHERE UserID=?", (user_id,))
        result = self.cursor.fetchone()
        if result is None:
            self.cursor.execute("INSERT INTO UserMessages VALUES (?, 1)", (user_id,))
        else:
            self.cursor.execute("UPDATE UserMessages SET MessageCount = MessageCount + 1 WHERE UserID=?", (user_id,))
        self.conn.commit()

    def cog_unload(self):
        self.conn.close()