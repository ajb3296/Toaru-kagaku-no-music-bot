import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context

from musicbot.utils.language import get_lan
from musicbot.utils.get_chart import get_melon, get_billboard, get_billboardjp
from musicbot import LOGGER, BOT_NAME_TAG_VER, COLOR_CODE


class Chart(commands.Cog, name="chart"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="chart",
        description="I will tell you from the 1st to the 10th place on the chart site",
    )
    @app_commands.describe(
        chart="Choose chart"
    )
    @app_commands.choices(chart=[
        app_commands.Choice(name="Melon", value="Melon"),
        app_commands.Choice(name="Billboard", value="Billboard"),
        app_commands.Choice(name="Billboard Japan", value="Billboard Japan")
    ])
    async def chart(self, ctx: Context, *, chart: str):
        """ I will tell you from the 1st to the 10th place on the chart site """
        await ctx.defer()

        title = None
        artist = None
        embed = None

        if chart is not None:
            chart = chart.upper()
        if chart == "MELON":
            title, artist = await get_melon(10)
            embed = discord.Embed(title=get_lan(ctx.author.id, "**멜론 차트**"), color=COLOR_CODE)
        elif chart == "BILLBOARD":
            title, artist = await get_billboard(10)
            embed = discord.Embed(title=get_lan(ctx.author.id, "**빌보드 차트**"), color=COLOR_CODE)
        elif chart == "BILLBOARD JAPAN":
            title, artist = await get_billboardjp(10)
            embed = discord.Embed(title=get_lan(ctx.author.id, "**빌보드 재팬 차트**"), color=COLOR_CODE)

        if embed is not None:
            if title is not None and artist is not None:
                for i in range(0, 10):
                    embed.add_field(name=str(i + 1) + ".", value=f"{artist[i]} - {title[i]}", inline=False)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Chart(bot))
    LOGGER.info("Chart loaded!")