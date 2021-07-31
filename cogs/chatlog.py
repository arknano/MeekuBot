import random
from discord import User
from discord.ext import commands
import csv
import typing
import markovify
import json
import os


class ChatLogCog(commands.Cog):

    def __init__(self, bot):
        local_path = os.path.dirname(__file__)
        self.bot = bot
        self.chatlog = list(csv.DictReader(open(os.path.join(local_path, os.pardir, 'logs/chatlog.tsv'), encoding="utf8"), delimiter="\t"))
        markovlines = ""
        line_count = 0
        for row in self.chatlog:
            markovlines += "\n" + row['Content']
            line_count += 1
        print(f'Processed {line_count} lines in chat history.')
        self.markov = markovify.NewlineText(markovlines, state_size=1)
        f = open(os.path.join(local_path, os.pardir, 'config/config.json'))
        self.config = json.load(f)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return

    @commands.command(name="nocontext", brief="Random shit we've said")
    async def _nocontext(self, ctx, arg: typing.Optional[User]):
        if arg is None:
            text = random.choice(list(self.chatlog))
            await ctx.send("Shit " + text['Author'].split("#")[0] + " says: \"" + text['Content'] + "\"")
        else:
            while True:
                text = random.choice(list(self.chatlog))
                print(text['AuthorID'] + " vs " + str(arg.id))
                if int(text['AuthorID']) == arg.id:
                    await ctx.send("Shit " + text['Author'].split("#")[0] + " says: \"" + text['Content'] + "\"")
                    break
                else:
                    continue

    @commands.command(name="nonsense", brief="Attempt to generate semi-coherent sentence based on chat history")
    async def _nonsense(self, ctx):
        await ctx.send(markov(self))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        r = random.random()
        if r < float(self.config['markovChance']):
            await message.channel.send(markov(self))

def setup(bot):
    bot.add_cog(ChatLogCog(bot))

def markov(self):
    return self.markov.make_sentence(min_words=self.config['minMarkovWords'], max_words=self.config['maxMarkovWords'],
                              max_overlap_ratio=self.config['markovOverlapRatio']).capitalize()