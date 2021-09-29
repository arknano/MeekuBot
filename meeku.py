from discord.ext import commands
import discord
from datetime import datetime
from functions.data import *
from discord.ext.commands import CommandNotFound
from functions.fun import *

token = load_tokens()
config = load_bot_config()
loc = load_loc()[config['language']]


def get_prefix(bot, message):
    prefixes = config['prefixes']
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix,
                   intents=discord.Intents.all(), case_insensitive=True)

initial_extensions = ['cogs.core', 'cogs.responses',
                      'cogs.gif', 'cogs.decide', 'cogs.chatlog', 'cogs.bot', 'cogs.admin']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    if config['devMode']:
        game = discord.Game("in dev mode with Graf. Last restart: " + datetime.now().strftime("%H:%M:%S"))
        await bot.change_presence(status=discord.Status.dnd, activity=game)
    else:
        game = discord.Game(config['playingStatus'])
        await bot.change_presence(status=discord.Status.online, activity=game)
    channel = bot.get_channel(config['botChannelID'])
    await channel.send(loc['botOnline'])
    print("Ready! Started at " + datetime.now().strftime("%H:%M:%S"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        if ctx.message.content.startswith("<"):
            text = await type_nonsense(ctx)
            await ctx.send(text)
            return
    raise error

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
