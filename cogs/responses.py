import discord
from discord.ext import commands
import random
import json
import os


class ResponsesCog(commands.Cog):

    def __init__(self, bot):
        local_path = os.path.dirname(__file__)
        self.bot = bot
        f = open(os.path.join(local_path, '..\\config\\responses.json'))
        self.responses = json.load(f)
        f = open(os.path.join(local_path, '..\\config\\config.json'))
        self.config = json.load(f)
        f = open(os.path.join(local_path, '..\\config\\emoji.json'), encoding="utf8")
        self.emoji = json.load(f)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        await naughty_mock(self, message)
        await fun_responses(self, message)
        await react(self, message)


async def naughty_mock(self, message):
    if "naughty" in [y.name.lower() for y in message.author.roles]:
        key = "im sorry meeku i love you"
        if message.content.lower() == key.lower():
            role = discord.utils.get(message.guild.roles, name='naughty')
            await message.author.remove_roles(role)
            await message.channel.send("Good.")
        else:
            await message.channel.send(sponge_mock(message.content))


async def fun_responses(self, message):
    for entry in self.responses:
        for trigger in self.responses[entry]['triggers']:
            if trigger in message.content.lower():
                if self.responses[entry]['chance'] > random.random():
                    await message.channel.send(random.choice(self.responses[entry]['responses']))
                    break


async def react(self, message):
    r = random.random()
    if r < float(self.config['reactChance']):
        if r < float(self.config['customEmojiChance']):
            emoji = random.choice(self.bot.emojis)
        else:
            emoji = random.choice(self.emoji['list'])['emoji']
            print(emoji)
        await message.add_reaction(emoji=emoji)


def setup(bot):
    bot.add_cog(ResponsesCog(bot))


def sponge_mock(input_text):
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
