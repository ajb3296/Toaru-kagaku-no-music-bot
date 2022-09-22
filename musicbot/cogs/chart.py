import discord
from discord.ext import commands
from discord.commands import slash_command, Option

from musicbot.utils.language import get_lan
from musicbot.utils.get_chart import get_melon, get_billboard, get_billboardjp
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Chart (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def chart(self, ctx, *, chart : Option(str, "Choose chart.", choices=["Melon", "Billboard", "Billboard Japan"])):
        """ I will tell you from the 1st to the 10th place on the chart site """
        await ctx.defer()

        if chart is not None:
            chart = chart.upper()
        if chart == "MELON":
            title, artist = await get_melon(10)
            embed=discord.Embed(title=get_lan(ctx.author.id, "chart_melon_chart"), color=color_code)
        elif chart == "BILLBOARD":
            title, artist = await get_billboard(10)
            embed=discord.Embed(title=get_lan(ctx.author.id, "chart_billboard_chart"), color=color_code)
        elif chart == "BILLBOARD JAPAN":
            title, artist = await get_billboardjp(10)
            embed=discord.Embed(title=get_lan(ctx.author.id, "chart_billboardjp_chart"), color=color_code)
        for i in range(0, 10):
            embed.add_field(name=str(i+1) + ".", value = f"{artist[i]} - {title[i]}", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.followup.send(embed=embed)

def setup (bot) :
    bot.add_cog (Chart (bot))
    LOGGER.info('Chart loaded!')
