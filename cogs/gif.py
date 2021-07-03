import discord
from discord.ext import commands
import TenGiphPy
import json


class GifCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        f = open('token.json')
        token = json.load(f)
        g = open('gif.json')
        self.gifJSON = json.load(g)
        self.tenor = TenGiphPy.Tenor(token=token['tenor_token'])

    @commands.command(
        name="aunty",
        brief="Post Aunty Donna gif"
    )
    async def _aunty(self, ctx, *, arg="a"):
        if arg.lower() == "broden":
            await ctx.send(self.tenor.random(tag=self.gifJSON['broden']))
        elif arg.lower() == "mark":
            await ctx.send(self.tenor.random(tag=self.gifJSON['mark']))
        elif arg.lower() == "zach":
            await ctx.send(self.tenor.random(tag=self.gifJSON['zach']))
        else:
            await ctx.send(self.tenor.random(tag=self.gifJSON['aunty']))


def setup(bot):
    bot.add_cog(GifCog(bot))
