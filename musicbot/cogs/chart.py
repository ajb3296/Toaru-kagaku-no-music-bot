import discord
from discord.ext import commands
from discord.commands import slash_command

from musicbot.utils.language import get_lan
from musicbot.utils.get_chart import *
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Chart (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self.melon_url = 'https://www.melon.com/chart/index.htm'
        self.billboard_url = 'https://www.billboard.com/charts/hot-100'
        self.billboardjp_url = 'https://www.billboard-japan.com/charts/detail?a=hot100'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    @slash_command()
    async def melon(self, ctx) :
        """ I will tell you from the 1st to the 10th place on the melon chart. """
        title, artist = await get_melon()
        embed=discord.Embed(title=get_lan(ctx.author.id, "chart_melon_chart"), color=color_code)
        for i in range(0, 10):
            embed.add_field(name=str(i+1) + ".", value = f"{artist[i]} - {title[i]}", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

    @slash_command()
    async def billboard(self, ctx) :
        """ I will tell you from the 1st to the 10th place on the billboard chart. """
        title, artist = await get_billboard()
        embed=discord.Embed(title=get_lan(ctx.author.id, "chart_billboard_chart"), color=color_code)
        for i in range(0, 10):
            embed.add_field(name=str(i+1) + ".", value = f"{artist[i]} - {title[i]}", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

    @slash_command()
    async def billboardjp(self, ctx) :
        """ I will tell you from the 1st to the 10th place on the billboard japan chart. """
        title, artist = await get_billboardjp()
        embed=discord.Embed(title=get_lan(ctx.author.id, "chart_billboard_chart"), color=color_code)
        for i in range(0, 10):
            embed.add_field(name=str(i+1) + ".", value = f"{artist[i]} - {title[i]}", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (Chart (bot))
    LOGGER.info('Chart loaded!')
