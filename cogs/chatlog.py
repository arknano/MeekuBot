import random
from discord import User
from discord.ext import commands
import csv
import typing


class ChatLogCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.chatlog = list(csv.DictReader(open('chatlog.tsv', encoding="utf8"), delimiter="\t"))
        line_count = 0
        for row in self.chatlog:
            line_count += 1
        print(f'Processed {line_count} lines in chat history.')

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


def setup(bot):
    bot.add_cog(ChatLogCog(bot))
