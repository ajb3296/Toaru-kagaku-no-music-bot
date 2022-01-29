import discord
from discord.ext import commands
from discord.commands import slash_command
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Ping (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def ping(self, ctx):
        """ Measure ping speed """
        latancy = self.bot.latency
        embed=discord.Embed(title="**Ping**", description=f':ping_pong: Pong! Discord latency {round(latancy * 1000)}ms', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)
        

def setup (bot) :
    bot.add_cog (Ping (bot))
    LOGGER.info('Ping loaded!')
