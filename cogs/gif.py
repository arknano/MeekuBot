from discord.ext import commands
import requests
import random
from functions.data import *


class GifCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.tenor_key = load_tokens()['tenor_token']
        self.gifJSON = load_gif_config()

    @commands.command(
        name="aunty",
        brief="Post Aunty Donna gif"
    )
    async def _aunty(self, ctx, *, arg=""):
        await ctx.send(tenor_random_gif(self, self.gifJSON['aunty'] + " " + str(arg)))

    @commands.command(
        name="miku",
        brief="Post Miku gif"
    )
    async def _miku(self, ctx, *, arg=""):
        await ctx.send(tenor_random_gif(self, self.gifJSON['miku'] + " " + str(arg)))

    @commands.command(
        name="monch",
        brief="do a hemckin big monch"
    )
    async def _monch(self, ctx):
        await ctx.send(self.gifJSON['monch'] )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        await  feature_complete(self, message)


async def feature_complete(self, message):
    key = "feature complete"
    if message.content.lower() == key.lower():
        await message.channel.send(self.gifJSON['featurecomplete'])


def tenor_random_gif(self, tag):
    request_string = "https://api.tenor.co/v1/random?q=\"{tag}\"&key={key}&limit=50&contentfilter=low"
    response = requests.get(request_string.format(key=self.tenor_key, tag=tag))
    results = json.loads(response.text)
    if len(results['results']) > 0:
        random_entry = random.choice(results['results'])
        gif = random_entry['media'][0]['gif']['url']
        return gif
    else:
        return "Nothing found! :("


def setup(bot):
    bot.add_cog(GifCog(bot))
