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
        await naughtyMock(self, message)
        await funResponses(self, message)


async def naughtyMock(self, message):
    if "naughty" in [y.name.lower() for y in message.author.roles]:
        if message.content == "im sorry meeku i love you":
            role = discord.utils.get(message.guild.roles, name='naughty')
            await message.author.remove_roles(role)
            await message.channel.send("Good.")
        else:
            await message.channel.send(spongemock(message.content))
    

async def funResponses(self, message):
    for entry in self.responses:
        for trigger in self.responses[entry]['triggers']:
            if (trigger in message.content.lower()):
                if (self.responses[entry]['chance'] > random.random()):
                    await message.channel.send(random.choice(self.responses[entry]['responses']))
                    break

def setup(bot):
    bot.add_cog(ResponsesCog(bot))

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