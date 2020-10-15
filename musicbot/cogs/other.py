import discord
import asyncio
from discord.ext import commands
from musicbot.utils.crawler import getReqTEXT
from bs4 import BeautifulSoup
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code, BOT_NAME, BOT_ID
import random
import platform
import psutil
from musicbot.utils.misc import footer
import subprocess

class Other (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
    
    @commands.command (name = '초대', aliases = ['invite'])
    async def invite(self, ctx):
        link = 'https://discord.com/oauth2/authorize?client_id=%s&permissions=3165184&scope=bot' %BOT_ID
        embed=discord.Embed(title="**절 당신이 관리하는 서버에 초대해주시다니!**", description="정말 감사합니다! [여기](<%s>)를 눌러 서버에 초대해주세요!" %link, color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)
        
    @commands.command (name = 'javaver', aliases = ['java', 'javaversion', '자바', '자바버전'])
    async def javaver(self, ctx):
        res = subprocess.check_output("java --version", shell=True, encoding='utf-8')
        embed=discord.Embed(title="**Java 버전**", description="```%s```" %res, color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.command (name = 'uptime', aliases = ['업타임'])
    async def uptime(self, ctx):
        res = subprocess.check_output("uptime", shell=True, encoding='utf-8')
        embed=discord.Embed(title="**Uptime**", description="```%s```" %res.replace(',  ', '\n').replace(', ', '\n').replace(': ', ' : ')[1:], color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Other (bot))
    LOGGER.info('Other loaded!')
