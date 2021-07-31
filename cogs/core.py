import discord
from discord.ext import commands
from discord import User
import random
from datetime import datetime
import json
import os


class CoreCog(commands.Cog):

    def __init__(self, bot):
        local_path = os.path.dirname(__file__)
        self.bot = bot
        f = open(os.path.join(local_path, '..\\config\\config.json'))
        self.config = json.load(f)
        f = open(os.path.join(local_path, '..\\config\\token.json'))
        token = json.load(f)
        self.adminID = token['admin']

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


def setup(bot):
    bot.add_cog(CoreCog(bot))
