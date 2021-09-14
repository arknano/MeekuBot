import discord
from discord.ext import commands
from discord.utils import get
from functions.data import *

class AdminCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.adminID = load_tokens()['admin']

    @commands.command(
        name="naughty",
        hidden=True
    )
    async def _naughty(self, ctx, user: discord.Member):
        if ctx.author.id != self.adminID: return
        if get(ctx.guild.roles, name="naughty"):
            role = discord.utils.find(lambda r: r.name == 'naughty', ctx.guild.roles)
            if role in user.roles:
                await user.remove_roles(role)
                await ctx.send("Fine...")
            else:
                await user.add_roles(discord.utils.get(ctx.guild.roles, name="naughty"))
                await ctx.send("Bad!")
        else:
            await ctx.send("There is no naughty role!")


def setup(bot):
    bot.add_cog(AdminCog(bot))
