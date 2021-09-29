import random
from discord import User
from discord.ext import commands
import typing
import sqlite3 as sql
from functions.data import *
from functions.fun import *


class ChatLogCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = load_bot_config()
        self.loc = load_loc()[self.config['language']]
        self.db = sql.connect(self.config['chatlogDB'])
        with self.db:
            cursor = self.db.cursor()
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS chatlog (
                    id integer NOT NULL,
                    nick text NOT NULL,
                    message text NOT NULL
                );
            """)
            cursor.execute("SELECT * FROM chatlog")

    @commands.command(name="nocontext", brief="Random shit we've said")
    async def _nocontext(self, ctx, arg: typing.Optional[User]):
        with self.db:
            cursor = self.db.cursor()
            if arg is None:
                cursor.execute("SELECT * FROM chatlog ORDER BY RANDOM() LIMIT 1;")
                data = cursor.fetchall()
                text = data[0]
            else:
                cursor.execute("SELECT * FROM chatlog WHERE id = " + str(arg.id))
                data = cursor.fetchall()
                text = random.choice(data)
        username = self.bot.get_user(text[0]).name
        if username == text[1]:
            name = text[1]
        else:
            name = "{0} ({1})".format(text[1], username)
        await ctx.send(self.loc['noContext'].format(user=name, message=text[2]))

    @commands.command(name="nonsense", brief="Attempt to generate semi-coherent sentence based on chat history")
    async def _nonsense(self, ctx):
        await ctx.send(markov())

    @commands.Cog.listener()
    async def on_message(self, message):
        r = random.random()
        if r < float(self.config['markovChance']):
            if message.author != self.bot.user:
                text = await type_nonsense(message)
                await message.channel.send(text)
        for prefix in self.config['prefixes']:
            if message.content.startswith(prefix): return
            if message.content.startswith("Shit ") and message.author == self.bot.user: return
        string = 'INSERT INTO chatlog (id, nick, message) values(?,?,?)'
        data = [
            (message.author.id, message.author.display_name, message.clean_content)
        ]
        with self.db:
            self.db.executemany(string, data)


def setup(bot):
    bot.add_cog(ChatLogCog(bot))
