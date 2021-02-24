import discord
from discord.ext import commands
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Ping (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (name = 'ping', aliases = ['핑'])
    async def ping(self, ctx):
        latancy = self.bot.latency
        embed=discord.Embed(title="**Ping**", description=f':ping_pong: Pong! {round(latancy * 1000)}ms', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Ping (bot))
    LOGGER.info('Ping loaded!')
