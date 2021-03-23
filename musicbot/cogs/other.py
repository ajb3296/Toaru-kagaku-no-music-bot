import discord
import lavalink
from discord.ext import commands
import platform
import subprocess

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Other (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
    
    @commands.command (name = '초대', aliases = ['invite', 'ㅊㄷ'])
    async def invite(self, ctx):
        link = 'https://discord.com/oauth2/authorize?client_id=%s&permissions=3165184&scope=bot' %self.bot.user.id
        embed=discord.Embed(title=get_lan(ctx.author.id, "other_invite_title"), description=get_lan(ctx.author.id, "other_invite_description").format(link=link), color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'color', aliases = ['컬러', '색깔'])
    async def color(self, ctx, arg):
        arg = arg.replace("#", "")
        if not arg[0:2] == "0x":
            arg =  "0x" + arg
        embed=discord.Embed(title="**당신이 고른 색깔은!**", description="이 색깔입니다!", color=int(arg, 0))
        red = hex(255 - int("0x"+str(arg[2:4]), 16))
        green = hex(255 - int("0x"+str(arg[4:6]), 16))
        blue = hex(255 - int("0x"+str(arg[6:8]), 16))
        txtcolor = red[2:4]+green[2:4]+blue[2:4]
        embed.set_image(url=f"https://dummyimage.com/300x200/{arg[2:]}/{txtcolor}/&text={arg[2:]}")
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'javaver', aliases = ['java', 'javaversion', '자바', '자바버전'])
    async def javaver(self, ctx):
        res = subprocess.check_output("java --version", shell=True, encoding='utf-8')
        embed=discord.Embed(title=get_lan(ctx.author.id, "other_java_ver"), description="```%s```" %res, color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'softver', aliases = ['버전', 'ver'])
    async def softver(self, ctx) :
        javaver = subprocess.check_output("java --version", shell=True, encoding='utf-8')
        lavalinkver = subprocess.check_output("java -jar Lavalink.jar --version", shell=True, encoding='utf-8')
        embed=discord.Embed(title=get_lan(ctx.author.id, "other_soft_ver"), color=color_code)
        embed.add_field(name="Python Ver", value=("%s %s") %(platform.python_implementation(), platform.python_version()), inline=False)
        embed.add_field(name="Discord.py Ver", value=discord.__version__, inline=False)
        embed.add_field(name="Lavalink.py Ver", value=lavalink.__version__, inline=False)
        embed.add_field(name="Java Ver", value=f"```{javaver}```", inline=False)
        embed.add_field(name="Lavalink Ver", value=f"```{lavalinkver}```", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'uptime', aliases = ['업타임'])
    async def uptime(self, ctx):
        res = subprocess.check_output("uptime", shell=False, encoding='utf-8')
        embed=discord.Embed(title=get_lan(ctx.author.id, "other_uptime"), description="```%s```" %res.replace(',  ', '\n').replace(', ', '\n').replace(': ', ' : ')[1:], color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Other (bot))
    LOGGER.info('Other loaded!')
