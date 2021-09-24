import discord
from discord.ext import commands
import random
import json
import os
from functions.fun import sponge_mock
from functions.data import *

class ResponsesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.responses = load_responses_config()
        self.config = load_bot_config()
        self.emoji = load_emoji_config()
        self.loc = load_loc()[self.config['language']]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        await naughty_mock(self, message)
        await fun_responses(self, message)
        await react(self, message)


async def naughty_mock(self, message):
    if "naughty" in [y.name.lower() for y in message.author.roles]:
        if message.content.lower() == self.config['naughtyApologiseString'].lower():
            role = discord.utils.get(message.guild.roles, name='naughty')
            await message.author.remove_roles(role)
            await message.channel.send(self.loc['naughtyApologised'])
        else:
            for prefix in self.config['prefixes']:
                if message.content.startswith(prefix):
                    return
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