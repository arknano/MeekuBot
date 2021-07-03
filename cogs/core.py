import discord
from discord.ext import commands
import random


class CoreCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="mi",
        brief="Is Meeku awake? Find out!"
    )
    async def _ping(self, ctx):
        await ctx.send(f"ku!")


def setup(bot):
    bot.add_cog(CoreCog(bot))
