import discord
from discord.ext import commands
import random
import json


class ResponsesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        f = open('responses.json')
        self.responses = json.load(f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        for entry in self.responses:
            for trigger in self.responses[entry]['triggers']:
                if (trigger in message.content.lower()):
                    if (self.responses[entry]['chance'] > random.random()):
                        await message.channel.send(random.choice(self.responses[entry]['responses']))
                        break


def setup(bot):
    bot.add_cog(ResponsesCog(bot))
