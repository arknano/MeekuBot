import sys
from datetime import datetime
from discord.ext import commands
import json
import typing
import os


class AdminCog(commands.Cog):

    def __init__(self, bot):
        local_path = os.path.dirname(__file__)
        self.bot = bot
        f = open(os.path.join(local_path, os.pardir, 'config/config.json'))
        self.config = json.load(f)
        f = open(os.path.join(local_path, os.pardir, 'config/token.json'))
        token = json.load(f)
        self.adminID = token['admin']
        f = open(os.path.join(local_path, os.pardir, 'config/responses.json'))
        self.responses = json.load(f)

    @commands.command(name="config", hidden=True)
    async def _config(self, ctx, mode, key, value: typing.Union[bool, int, float, str] = "NULL"):
        if ctx.author.id == self.adminID:
            # config.json
            if key in self.config:
                if mode == "set":
                    if value == "NULL":
                        await ctx.send("You need to provide a value!")
                    else:
                        if isinstance(self.config[key], str):
                            if type(value) is not str:
                                await ctx.send("Umm... Try a string!")
                                return
                            else:
                                self.config[key] = str(value)
                        elif isinstance(self.config[key], bool):
                            if type(value) is not bool:
                                await ctx.send("Umm... Try a bool!")
                                return
                            else:
                                self.config[key] = bool(value)
                        elif isinstance(self.config[key], int):
                            if type(value) is not int:
                                await ctx.send("Umm... Try an int!")
                                return
                            else:
                                self.config[key] = int(value)
                        elif isinstance(self.config[key], float):
                            if type(value) is not float:
                                await ctx.send("Umm... Try a float!")
                                return
                            else:
                                self.config[key] = float(value)
                        else:
                            await ctx.send("Aborting!")
                            return
                        file = open('config/config.json', "w")
                        json.dump(self.config, file, indent=4)
                        file.close()
                        await ctx.send("Ok, I set " + key + " to " + str(value) + "! Don't forget to reload!")
                elif mode == "get":
                    await ctx.send("`" + key + ": " + str(self.config[key]) + "`")
                else:
                    await ctx.send("Huh?")
            # responses.json
            elif key in self.responses:
                if mode == "set":
                    if value == "NULL":
                        await ctx.send("You need to provide a value!")
                    else:
                        if type(value) is not float:
                            await ctx.send("Umm... Try a float!")
                            return
                        else:
                            self.responses[key]['chance'] = float(value)
                        file = open('config/responses.json', "w")
                        json.dump(self.responses, file, indent=4)
                        file.close()
                        await ctx.send("Ok, I set " + key + " to " + str(value) + "! Don't forget to reload!")
                elif mode == "get":
                    await ctx.send("`" + key + ": " + str(self.responses[key]['chance']) + "`")
                else:
                    await ctx.send("Huh?")
            else:
                await ctx.send("That key doesn't exist!")

        else:
            await ctx.send("No!")

    @commands.command(name='reload', hidden=True)
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        if ctx.author.id == self.adminID:
            try:
                self.bot.unload_extension(module)
                self.bot.load_extension(module)
            except Exception as e:
                await ctx.send('{}: {}'.format(type(e).__name__, e))
            else:
                await ctx.send("Ok, reloaded " + module + "!")

    @commands.command(name="restart", hidden=True)
    async def _restart(self, ctx):
        if ctx.author.id == self.adminID:
            await ctx.send("Ok, brb!")
            # if sys.platform.startswith('linux'):
            #     os.system("clear")
            # else:
            #     os.system("cls")
            print("Restart command recieved at " + datetime.now().strftime("%H:%M:%S"))
            if self.config['serverMode']:
                os.execl(sys.executable, "python3.9" + " meeku.py")
            else:
                os.execl(sys.executable, "python" + " meeku.py")
        else:
            await ctx.send("No!")

def setup(bot):
    bot.add_cog(AdminCog(bot))
