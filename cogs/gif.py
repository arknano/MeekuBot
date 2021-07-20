import discord
from discord.ext import commands
import json
import requests
import random


class GifCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        f = open('token.json')
        token = json.load(f)
        self.tenor_key = token['tenor_token']
        g = open('gif.json')
        self.gifJSON = json.load(g)

    @commands.command(
        name="aunty",
        brief="Post Aunty Donna gif"
    )
    async def _aunty(self, ctx, *, arg="a"):
        if arg.lower() == "broden":
            await ctx.send(tenor_random_gif(self, self.gifJSON['broden']))
        elif arg.lower() == "mark":
            await ctx.send(tenor_random_gif(self, self.gifJSON['mark']))
        elif arg.lower() == "zach":
            await ctx.send(tenor_random_gif(self, self.gifJSON['zach']))
        else:
            await ctx.send(tenor_random_gif(self, self.gifJSON['aunty']))

    @commands.command(
        name="miku",
        brief="Post Miku gif"
    )
    async def _miku(self, ctx):
        await ctx.send(tenor_random_gif(self, self.gifJSON['miku']))

    @commands.command(
        name="monch",
        brief="do a hemckin big monch"
    )
    async def _monch(self, ctx):
        await ctx.send(self.gifJSON['monch'])


def tenor_random_gif(self, tag):
    request_string = "https://api.tenor.co/v1/random?q=\"{tag}\"&key={key}&limit=50&contentfilter=low"
    response = requests.get(request_string.format(key=self.tenor_key, tag=tag))
    print(request_string.format(key=self.tenor_key, tag=tag))
    print(response)
    results = json.loads(response.text)
    print(results)
    random_entry = random.choice(results['results'])
    gif = random_entry['media'][0]['gif']['url']
    return gif


def setup(bot):
    bot.add_cog(GifCog(bot))
