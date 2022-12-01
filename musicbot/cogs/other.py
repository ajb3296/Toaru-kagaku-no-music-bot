import time
import psutil
import discord
import lavalink
import platform
import datetime
import subprocess
from discord.ext import commands
from discord.commands import slash_command

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Other (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def invite(self, ctx):
        """ Send you a link for invite me """
        link = f'https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=414501391424&scope=bot%20applications.commands'
        embed=discord.Embed(title=get_lan(ctx.author.id, "other_invite_title"),
                            description=get_lan(ctx.author.id, "other_invite_description").format(link=link),
                            color=color_code
        )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

    @slash_command()
    async def softver(self, ctx) :
        """ Let me tell you the version of the modules! """
        javaver = subprocess.check_output('java --version', stderr=subprocess.STDOUT, encoding='utf-8')
        lavalinkver = subprocess.check_output('java -jar Lavalink.jar', stderr=subprocess.STDOUT, encoding='utf-8')
        embed=discord.Embed(title=get_lan(ctx.author.id, "other_soft_ver"), color=color_code)
        embed.add_field(name="Python Ver", value=("%s %s") %(platform.python_implementation(), platform.python_version()), inline=False)
        embed.add_field(name="Discord.py Ver", value=discord.__version__, inline=False)
        embed.add_field(name="Lavalink.py Ver", value=lavalink.__version__, inline=False)
        embed.add_field(name="Java Ver", value=f"```{javaver}```", inline=False)
        embed.add_field(name="Lavalink Ver", value=f"```{lavalinkver}```", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

    @slash_command()
    async def uptime(self, ctx):
        """ Let me tell you the server's uptime! """
        uptime_string = str(datetime.timedelta(seconds=int(time.time() - psutil.boot_time())))
        embed=discord.Embed(title=get_lan(ctx.author.id, "other_uptime"),
                            description=f"```{uptime_string}```",
                            color=color_code)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (Other (bot))
    LOGGER.info('Other loaded!')
