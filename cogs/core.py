import discord
from discord.ext import tasks, commands
from discord import User
import random
from datetime import datetime
import json
import os
import sqlite3 as sql
from ctparse import ctparse


class CoreCog(commands.Cog):

    def __init__(self, bot):
        local_path = os.path.dirname(__file__)
        self.bot = bot
        f = open(os.path.join(local_path, os.pardir, 'config/config.json'))
        self.config = json.load(f)
        f = open(os.path.join(local_path, os.pardir, 'config/token.json'))
        token = json.load(f)
        self.adminID = token['admin']
        self.hydrate.start()
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
        self.remind.start()

    @commands.command(name="mi", brief="Is Meeku awake? Find out!")
    async def _ping(self, ctx):
        await ctx.send("ku!")

    @commands.command(name="mock", brief="Spongebob meme your words")
    async def _mock(self, ctx):
        message = ctx.message.content.replace(
            ctx.prefix + ctx.invoked_with + " ", "")
        await ctx.send(spongemock(message))

    @commands.command(name="slap", brief="Slap someone with a fish-based entity")
    async def _slap(self, ctx, user: User):
        if user is self.bot.user:
            await ctx.send(
                self.bot.user.mention + " slaps " + ctx.message.author.mention + " about a bit with a large trout instead.")
        else:
            await ctx.send(ctx.message.author.mention + " slaps " + user.mention + " about a bit with a large trout.")

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
            await channel.send("@here Daily reminder to stay hydrated!")

    @hydrate.before_loop
    async def before_hydrate(self):
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=1.0)
    async def remind(self):
        self.hydrate.change_interval(minutes=random.randrange(50, 70))
        if datetime.now().minute == self.config['hydrateRemindHour']:
            channel = self.bot.get_channel(self.config['generalChannelID'])
            # await channel.send("@here Daily reminder to stay hydrated!")

    @remind.before_loop
    async def before_remind(self):
        await self.bot.wait_until_ready()

    @commands.command(name="remind")
    async def _remind(self, ctx, *, arg="OVERRIDEXXX"):
        if arg == "OVERRIDEXXX":
            await ctx.send("Huh?")
            return
        args = ctx.message.content.split(" ", 2)
        if args[1].lower() == "me":
            user = ctx.message.author
            print(user)
        else:
            user = await getUserFromMention(ctx, args[1])
            print(user)
            if user is None:
                await ctx.send("Who am I supposed to be reminding? Try again!")
                return
        if len(args) == 2:
            if user == ctx.message.author:
                await ctx.send("Remind you when? Remind you what???")
            elif user == self.bot.user:
                await ctx.send("Remind me when? Remind me what???")
            else:
                await ctx.send("Remind them when? Remind them what???")
            return
        content = args[2].split(" to ", 1)
        if len(content) == 1:
            await ctx.send("That's not how this works.")
            return
        now = datetime.now()
        t = ctparse(content[0], ts=now).resolution
        dt = datetime(t.year, t.month, t.day, t.hour or 0, t.minute or 0)
        if user == ctx.message.author:
            name = "you"
        else:
            name = user.display_name
        await ctx.send("Ok, I'll remind {0} at {1} to {2}".format(name, dt, content[1]))

def spongemock(input_text):
    output_text = ""
    for char in input_text:
        if char.isalpha():
            if random.random() > 0.5:
                output_text += char.upper()
            else:
                output_text += char.lower()
        else:
            output_text += char
    return output_text

async def getUserFromMention(ctx, mention):
    mention = mention.replace("<", "")
    mention = mention.replace(">", "")
    id = mention.replace("@!", "")
    return await ctx.guild.fetch_member(id)

def setup(bot):
    bot.add_cog(CoreCog(bot))
