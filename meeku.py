# import discord
from discord.ext import commands
import discord
import json
from datetime import datetime

f = open('config/token.json')
token = json.load(f)


def get_prefix(bot, message):
    prefixes = ['!', '.']
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix,
                   intents=discord.Intents.default(), case_insensitive=True)

initial_extensions = ['cogs.core', 'cogs.responses',
                      'cogs.gif', 'cogs.decide', 'cogs.chatlog']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    game = discord.Game("in dev mode with Graf. Last restart: " + datetime.now().strftime("%H:%M:%S"))
    await bot.change_presence(status=discord.Status.dnd, activity=game)
    print("Ready!")


# slash = SlashCommand(bot, sync_commands=True)
# guild_ids = [819745580309413919]  # Put your server ID in this array.
# @slash.slash(
#     name="saybanany",
#     description="Say it!!!",
#     guild_ids=guild_ids
# )
# async def _banany(ctx):
#     await ctx.send(f"Banany!")

bot.run(token['discord_token'])
