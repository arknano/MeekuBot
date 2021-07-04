import discord
from discord.ext import commands
import requests

# Barely functional, no missing entry checks. mothballed


class MusicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="song",
        brief="Retrieve streaming links"
    )
    async def _song(self, ctx, *, arg):
        args = arg.split(" ", 1)
        response = requests.get(
            "https://api.song.link/v1-alpha.1/links?url=" + args[0] + "&userCountry=AU")
        json = response.json()
        embed = discord.Embed(title="is sharing a song!", description=args[1])
        embed.set_author(name=ctx.message.author.name,
                         icon_url=ctx.message.author.avatar_url)
        embed.set_footer(text="Powered by song.link")
        spoftyLink = "[Spotify](" + \
            json["linksByPlatform"]["spotify"]["url"] + ")"
        appleLink = "[Apple Music](" + \
            json["linksByPlatform"]["appleMusic"]["url"] + ")"
        ytMusicLink = "[YouTube Music](" + \
            json["linksByPlatform"]["youtubeMusic"]["url"] + ")"
        embed.add_field(name="Links", value=spoftyLink + " | " +
                        appleLink + " | " + ytMusicLink)
        await ctx.send(embed=embed)
        await ctx.send(json["linksByPlatform"]["youtube"]["url"])
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(MusicCog(bot))
