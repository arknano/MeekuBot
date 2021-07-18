import discord
from discord.ext import commands
from discord import User
import random


class CoreCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mi", brief="Is Meeku awake? Find out!")
    async def _ping(self, ctx):
        await ctx.send(f"ku!")

    @commands.command(name="mock", brief="Spongebob meme your words")
    async def _mock(self, ctx):
        message = ctx.message.content.replace(
            ctx.prefix + ctx.invoked_with + " ", "")
        await ctx.send(spongemock(message))

    @commands.command(name="slap", brief="Slap someone with a fish-based entity")
    async def _slap(self, ctx, user: User):
        if (user is self.bot.user):
            await ctx.send(self.bot.user.mention + " slaps " + ctx.message.author.mention + " about a bit with a large trout instead.")
        else:
            await ctx.send(ctx.message.author.mention + " slaps " + user.mention + " about a bit with a large trout.")


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
