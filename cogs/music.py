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
        spofty_link = "[Spotify](" + \
                      json["linksByPlatform"]["spotify"]["url"] + ")"
        apple_link = "[Apple Music](" + \
                     json["linksByPlatform"]["appleMusic"]["url"] + ")"
        yt_music_link = "[YouTube Music](" + \
                        json["linksByPlatform"]["youtubeMusic"]["url"] + ")"
        embed.add_field(name="Links", value=spofty_link + " | " +
                                            apple_link + " | " + yt_music_link)
        await ctx.send(embed=embed)
        await ctx.send(json["linksByPlatform"]["youtube"]["url"])
        await self.bot.delete_message(ctx.message)


def setup(bot):
    bot.add_cog(MusicCog(bot))
