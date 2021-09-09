import random
from discord import User
from discord.ext import commands
import csv
import typing
import markovify
import json
import os
import sqlite3 as sql


class ChatLogCog(commands.Cog):

    def __init__(self, bot):
        local_path = os.path.dirname(__file__)
        self.bot = bot

        f = open(os.path.join(local_path, os.pardir, 'config/config.json'))
        self.config = json.load(f)
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
            data = cursor.fetchall()
            markovlines = ""
            line_count = 0
            for row in data:
                markovlines += "\n" + row[2] + ""
                line_count += 1
            print(f'Processed {line_count} lines in chat history.')
            self.markov = markovify.NewlineText(markovlines, state_size=1)

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
        await ctx.send("Shit {0} says: \"{1}\"".format(name, text[2]))

    @commands.command(name="nonsense", brief="Attempt to generate semi-coherent sentence based on chat history")
    async def _nonsense(self, ctx):
        await ctx.send(markov(self))

    @commands.Cog.listener()
    async def on_message(self, message):
        r = random.random()
        if r < float(self.config['markovChance']):
            if message.author != self.bot.user:
                await message.channel.send(markov(self))
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


def markov(self):
    string = self.markov.make_sentence(min_words=self.config['minMarkovWords'], max_words=self.config['maxMarkovWords'],
                                     max_overlap_ratio=self.config['markovOverlapRatio'], tries=100)
    return string.capitalize()
