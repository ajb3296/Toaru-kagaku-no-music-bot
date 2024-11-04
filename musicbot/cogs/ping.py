import time
import discord
from discord.ext import commands
from discord.ext.commands import Context

from musicbot import LOGGER, BOT_NAME_TAG_VER, COLOR_CODE


class Ping(commands.Cog, name="ping"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="ping",
        description="Measure ping speed"
    )
    async def ping(self, ctx: Context):
        """Measure ping speed"""
        await ctx.defer()

        latency = self.bot.latency
        before = time.monotonic()

        embed = discord.Embed(
            title="**Ping**",
            description=f'🏓 Pong! WebSocket Ping {round(latency * 1000)}ms\n🏓 Pong! Measuring...',
            color=COLOR_CODE
        )
        embed.set_footer(text=BOT_NAME_TAG_VER)

        # 첫 메시지 전송
        message = await ctx.send(embed=embed)

        # 핑 측정
        ping = (time.monotonic() - before) * 1000

        # 수정된 임베드
        embed = discord.Embed(
            title="**Ping**",
            description=f'🏓 Pong! WebSocket Ping {round(latency * 1000)}ms\n🏓 Pong! Message Ping {int(ping)}ms',
            color=COLOR_CODE
        )
        embed.set_footer(text=BOT_NAME_TAG_VER)

        # 메시지 수정
        await message.edit(embed=embed)


async def setup(bot):
    await bot.add_cog(Ping(bot))
    LOGGER.info('Ping loaded!')
