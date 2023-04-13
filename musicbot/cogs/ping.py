import time
import discord
from discord.ext import commands
from discord.commands import slash_command
from musicbot import LOGGER, BOT_NAME_TAG_VER, COLOR_CODE

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    async def ping(self, ctx):
        """ Measure ping speed """
        latancy = self.bot.latency
        before = time.monotonic()
        embed=discord.Embed(title="**Ping**",
                            description=f'ping_pong: Pong! WebSocket Ping {round(latancy * 1000)}ms\n:ping_pong: Pong! Measuring...',
                            color=COLOR_CODE
        )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        message = await ctx.respond(embed=embed)
        ping = (time.monotonic() - before) * 1000
        embed=discord.Embed(title="**Ping**",
                            description=f':ping_pong: Pong! WebSocket Ping {round(latancy * 1000)}ms\n:ping_pong: Pong! Message Ping {int(ping)}ms',
                            color=COLOR_CODE
        )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await message.edit_original_message(embed=embed)

def setup (bot):
    bot.add_cog(Ping(bot))
    LOGGER.info('Ping loaded!')
