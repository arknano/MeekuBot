import discord
from discord.ext import tasks, commands
from discord import User
import random
from datetime import datetime
import sqlite3 as sql
from ctparse import ctparse
from functions.fun import sponge_mock
from functions.data import *


class CoreCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = load_bot_config()
        self.loc = load_loc()[self.config['language']]
        self.adminID = load_tokens()['admin']
        self.hydrate.start()
        self.db = sql.connect(self.config['remindersDB'])
        with self.db:
            cursor = self.db.cursor()
            self.db.execute("""
                CREATE TABLE IF NOT EXISTS reminders (
                    setTimestamp integer NOT NULL,
                    authorID integer NOT NULL,
                    targetID integer NOT NULL,
                    timestamp integer NOT NULL,
                    message text NOT NULL
                );
            """)
        self.remind.start()

    @commands.command(name="mi", brief="Is Meeku awake? Find out!")
    async def _ping(self, ctx):
        await ctx.send("ku!")

    @commands.command(name="mock", brief="Spongebob meme your words")
    async def _mock(self, ctx):
        message = ctx.message.content.replace(
            ctx.prefix + ctx.invoked_with + " ", "")
        await ctx.send(sponge_mock(message))

    @commands.command(name="slap", brief="Slap someone with a fish-based entity")
    async def _slap(self, ctx, user: User):
        if user is self.bot.user:
            await ctx.send(
                self.loc["slapMeeku"].format(meeku=self.bot.user.mention, author=ctx.message.author.mention))
        else:
            await ctx.send(self.loc["slap"].format(author=ctx.message.author.mention, target=user.mention))

    @commands.command(name="whois", brief="Get totally useless data about a user because this isn't irc")
    async def _whois(self, ctx, user: User):
        time_between = datetime.now() - user.created_at
        days_between = round(divmod(time_between.total_seconds(), 86400)[0])
        years_between = days_between // 365
        days_left = days_between % 365
        datestring = "Date created: " + user.created_at.strftime("%m/%d/%Y") + " (" + str(
            years_between) + " years and " + str(days_left) + " days old)"
        embed = discord.Embed(title=user.display_name, description=datestring)
        embed.set_author(name=user.name + "#" + user.discriminator, url=user.avatar_url, icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="ID", value=user.id)
        await ctx.send(embed=embed)

    @tasks.loop(minutes=60.0)
    async def hydrate(self):
        self.hydrate.change_interval(minutes=random.randrange(50, 70))
        if datetime.now().hour == self.config['hydrateRemindHour']:
            channel = self.bot.get_channel(self.config['generalChannelID'])
            await channel.send(self.loc['hydrate'])

    @hydrate.before_loop
    async def before_hydrate(self):
        await self.bot.wait_until_ready()

    @tasks.loop(seconds=30.0)
    async def remind(self):
        with self.db:
            cursor = self.db.cursor()
            cursor.execute('SELECT * FROM reminders')
            rows = cursor.fetchall()
            for row in rows:
                if row[3] <= datetime.now().timestamp():
                    mention = self.bot.get_user(row[2]).mention
                    channel = self.bot.get_channel(self.config['generalChannelID'])
                    if row[1] == row[2]:
                        await channel.send(self.loc['selfRemind'].format(author=mention, message=row[4]))
                    else:
                        author = self.bot.get_user(row[1]).mention
                        await channel.send(self.loc['remind'].format(target=mention, author=author, message=row[4]))
                    cursor.execute("DELETE FROM reminders WHERE setTimestamp=?", (row[0],))


    @remind.before_loop
    async def before_remind(self):
        await self.bot.wait_until_ready()

    @commands.command(name="remind")
    async def _remind(self, ctx, *, arg="OVERRIDEXXX"):
        if arg == "OVERRIDEXXX":
            await ctx.send(self.loc['remindSetupNoArgs'])
            return
        args = ctx.message.content.split(" ", 2)
        if args[1].lower() == "me":
            user = ctx.message.author
        else:
            user = await getUserFromMention(ctx, args[1])
            if user is None:
                await ctx.send(self.loc['remindSetupBadUser'])
                return
        if len(args) == 2:
            await ctx.send(self.loc['remindSetupBadArgs'])
            return
        content = args[2].split(";", 1)
        if len(content) == 1:
            await ctx.send(self.loc['remindSetupSemicolon'])
            return
        now = datetime.now()
        t = ctparse(content[0], ts=now).resolution
        dt = datetime(t.year, t.month, t.day, t.hour or 0, t.minute or 0)
        string = 'INSERT INTO reminders (setTimestamp, authorID, targetID, timestamp, message) values(?,?,?,?,?)'
        data = [
            (datetime.now().timestamp(), ctx.message.author.id, user.id, dt.timestamp(), content[1].strip())
        ]
        with self.db:
            self.db.executemany(string, data)

        if user == ctx.message.author:
            name = "you"
        else:
            name = user.display_name
        await ctx.send(self.loc['remindSetupAck'].format(target=name, time=dt, message=content[1].strip()))

async def getUserFromMention(ctx, mention):
    mention = mention.replace("<", "")
    mention = mention.replace(">", "")
    id = mention.replace("@!", "")
    return await ctx.guild.fetch_member(id)

def setup(bot):
    bot.add_cog(CoreCog(bot))
