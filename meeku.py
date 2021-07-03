# import discord
from discord.ext import commands
from discord_slash import SlashCommand
import discord
import json


f = open('token.json')
token = json.load(f)


def get_prefix(bot, message):
    prefixes = ['!']
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix,
                   intents=discord.Intents.default(), case_insensitive=True)


initial_extensions = ['cogs.core', 'cogs.responses', 'cogs.gif', 'cogs.decide']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Ready!")

#slash = SlashCommand(bot, sync_commands=True)
# guild_ids = [819745580309413919]  # Put your server ID in this array.
# @slash.slash(
#     name="saybanany",
#     description="Say it!!!",
#     guild_ids=guild_ids
# )
# async def _banany(ctx):
#     await ctx.send(f"Banany!")

bot.run(token['discord_token'])
