from discord.ext import commands
import random
from functions.data import *


class DecideCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.responses = load_decide_config()

    @commands.command(
        name="decide",
        aliases=['decision', 'choice', 'choose'],
        brief="Pick from options or answer yes or no"
    )
    async def _decide(self, ctx, *, arg="OVERRIDEXXX"):
        choices = ctx.message.content.split(" or ")
        if arg == "OVERRIDEXXX" or len(choices) == 1:
            if random.getrandbits(1):
                await ctx.message.channel.send(random.choice(self.responses['yes']))
            else:
                await ctx.message.channel.send(random.choice(self.responses['no']))
        else:
            choices[0] = choices[0].replace(
                ctx.prefix + ctx.invoked_with + " ", "")
            response = random.choice(self.responses['decide'])
            choice = random.choice(choices)
            await ctx.message.channel.send(response.format(choice=choice))


def setup(bot):
    bot.add_cog(DecideCog(bot))
