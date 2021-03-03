import time
import discord
from discord.ext import commands
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Ping (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (name = 'ping', aliases = ['핑'])
    async def ping(self, ctx):
        latancy = self.bot.latency
        before = time.monotonic()
        embed=discord.Embed(title="**Ping**", description=f'ping_pong: Pong! WebSocket Ping {round(latancy * 1000)}ms\n:ping_pong: Pong! 측정중...', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        message = await ctx.send(embed=embed)
        ping = (time.monotonic() - before) * 1000
        embed=discord.Embed(title="**Ping**", description=f':ping_pong: Pong! WebSocket Ping {round(latancy * 1000)}ms\n:ping_pong: Pong! Message Ping {int(ping)}ms', color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await message.edit(embed=embed)

def setup (bot) :
    bot.add_cog (Ping (bot))
    LOGGER.info('Ping loaded!')