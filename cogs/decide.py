from discord.ext import commands
import random
from functions.data import *
import sqlite3 as sql
from urllib.request import urlopen
import validators

class DecideCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = load_bot_config()
        self.loc = load_loc()[self.config['language']]
        self.strings = self.loc['decide']
        self.adminID = load_tokens()['admin']
        self.db = sql.connect(self.config['botDB'])
        with self.db:
            cursor = self.db.cursor()
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS choose (
                    authorID integer NOT NULL,
                    url text NOT NULL PRIMARY KEY,
                    key text NOT NULL
                );
            """)

    @commands.command(
        name="decide",
        brief="Pick from options or answer yes or no"
    )
    async def _decide(self, ctx, *, arg="OVERRIDEXXX"):
        choices = ctx.message.content.split(" or ")
        if arg == "OVERRIDEXXX" or len(choices) == 1:
            if random.getrandbits(1):
                await ctx.message.channel.send(random.choice(self.strings['yes']))
            else:
                await ctx.message.channel.send(random.choice(self.strings['no']))
        else:
            choices[0] = choices[0].replace(
                ctx.prefix + ctx.invoked_with + " ", "")
            response = random.choice(self.strings['decide'])
            choice = random.choice(choices)
            await ctx.message.channel.send(response.format(choice=choice))

    @commands.command(
        name="choose",
        brief="Pick from a predefined list of options"
    )
    async def _choose(self, ctx, *, arg="OVERRIDEXXX"):
        if arg == "OVERRIDEXXX":
            await ctx.send(self.strings['chooseNoArgument'])
            return
        args = ctx.message.content.split(" ", 4)
        if args[1].lower() == "add":
            if args[2].lower() == "add":
                await ctx.send(self.strings['chooseRestrictedKey'])
            else:
                if not args[3].endswith(".txt"):
                    await ctx.send(self.strings['chooseNotTXT'])
                    return
                if not validators.url(args[3]):
                    await ctx.send(self.strings['chooseInvalidURL'])
                    return
                with self.db:
                    cursor = self.db.cursor()
                    cursor.execute('SELECT url FROM choose WHERE key=\'{key}\';'.format(key=args[2].lower()))
                    if cursor.fetchone():
                        await ctx.send(self.strings['chooseDuplicateKey'])
                        return
                    string = 'INSERT INTO choose (authorID, url, key) values(?,?,?)'
                    data = [
                        (ctx.message.author.id, args[3], args[2].lower())
                    ]
                    self.db.executemany(string, data)
                    await ctx.send(self.strings['chooseAddSuccess'])
        elif args[1].lower() == "delete":
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('SELECT url FROM choose WHERE key=\'{key}\';'.format(key=args[2].lower()))
                row = cursor.fetchone()
                if row:
                    if ctx.author.id == self.adminID or ctx.author.id == row[0]:
                        cursor.execute('DELETE FROM choose WHERE key=\'{key}\';'.format(key=args[2].lower()))
                        await ctx.send(self.strings['chooseDeleteSuccess'])
                        return
                    else:
                        await ctx.send(self.strings['chooseDeleteReject'])
                        return
                else:
                    await ctx.send(self.strings['chooseKeyNotFound'])
        else:
            with self.db:
                cursor = self.db.cursor()
                cursor.execute('SELECT url FROM choose WHERE key=\'{key}\';'.format(key=args[1].lower()))
                row = cursor.fetchone()
                if row is None:
                    await ctx.send(self.strings['chooseKeyNotFound'])
                    return
                choices = urlopen(row[0]).readlines()
                response = random.choice(self.strings['decide'])
                choice = random.choice(choices)
                await ctx.message.channel.send(response.format(choice=choice.decode('utf-8', 'replace').strip()))


def setup(bot):
    bot.add_cog(DecideCog(bot))
