import discord
from bs4 import BeautifulSoup
from discord.ext import commands

from musicbot.utils.language import get_lan
from musicbot.utils.crawler import getReqTEXT
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Chart (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self.melon_url = 'https://www.melon.com/chart/index.htm'
        self.billboard_url = 'https://www.billboard.com/charts/hot-100'
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    @commands.command(name = '멜론', aliases = ['멜론차트', 'melonchart'])
    async def melon(self, ctx) :
        data = await getReqTEXT (self.melon_url, self.header)
        parse = BeautifulSoup(data, 'lxml')
        titles = parse.find_all("div", {"class": "ellipsis rank01"})
        songs = parse.find_all("div", {"class": "ellipsis rank02"})
        title = []
        song = []
        for t in titles:
            title.append(t.find('a').text)
        for s in songs:
            song.append(s.find('span', {"class": "checkEllipsis"}).text)
        embed=discord.Embed(title=get_lan(ctx.author.id, "chart_melon_chart"), color=color_code)
        for i in range(0, 10):
            embed.add_field(name=str(i+1) + ".", value = f"{song[i]} - {title[i]}", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command(name = '빌보드', aliases = ['빌보드차트', 'billboardchart'])
    async def billboard(self, ctx) :
        data = await getReqTEXT (self.billboard_url, self.header)
        parse = BeautifulSoup(data, 'lxml')
        # 음악명
        titles = parse.find_all("span", {"class" : "chart-element__information__song text--truncate color--primary"})
        # 아티스트
        songs = parse.find_all("span", {"class" : "chart-element__information__artist text--truncate color--secondary"})
        title = []
        song = []
        for t in titles:
            title.append(t.get_text())
        for s in songs:
            song.append(s.get_text())
        embed=discord.Embed(title=get_lan(ctx.author.id, "chart_billboard_chart"), color=color_code)
        for i in range(0, 10):
            embed.add_field(name=str(i+1) + ".", value = f"{song[i]} - {title[i]}", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Chart (bot))
    LOGGER.info('Chart loaded!')
