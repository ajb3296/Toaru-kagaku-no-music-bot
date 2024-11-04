import discord
import lavalink
import platform
import psutil
import math
import requests

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from musicbot.utils.language import get_lan
from musicbot.utils.paginator import Paginator
from musicbot import LOGGER, COLOR_CODE, BOT_NAME_TAG_VER, EXTENSIONS, DEBUG_SERVER


class Owners(commands.Cog, name="owners"):
    def __init__(self, bot):
        self.bot = bot
        self._last_members = None
        self.color = COLOR_CODE
        self.error_color = 0xff4a4a

    @commands.hybrid_command(
        name="dev_help",
        description="개발자용 도움말"
    )
    @commands.is_owner()
    @commands.guild_only()
    @app_commands.guilds(*DEBUG_SERVER)
    async def dev_help(self, ctx: Context):
        """ 개발자용 도움말 """
        embed = discord.Embed(title=get_lan(ctx.author.id, "help_dev"),
                              description=get_lan(ctx.author.id, "help_dev_description"), color=COLOR_CODE)
        embed.add_field(name=get_lan(ctx.author.id, "help_dev_serverlist_command"),
                        value=get_lan(ctx.author.id, "help_dev_serverlist_info"), inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "help_dev_modules_command"),
                        value=get_lan(ctx.author.id, "help_dev_modules_info"), inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "help_dev_load_command"),
                        value=get_lan(ctx.author.id, "help_dev_load_info"), inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "help_dev_unload_command"),
                        value=get_lan(ctx.author.id, "help_dev_unload_info"), inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "help_dev_reload_command"),
                        value=get_lan(ctx.author.id, "help_dev_reload_info"), inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "help_dev_serverinfo_command"),
                        value=get_lan(ctx.author.id, "help_dev_serverinfo_info"), inline=False)
        embed.add_field(name=get_lan(ctx.author.id, "help_dev_broadcast_command"),
                        value=get_lan(ctx.author.id, "help_dev_broadcast_info"), inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="load",
        description="모듈을 로드합니다."
    )
    @app_commands.describe(
        module="로드할 모듈을 입력해주세요"
    )
    @commands.is_owner()
    @commands.guild_only()
    @app_commands.guilds(*DEBUG_SERVER)
    async def load(self, ctx: Context, module: str):
        """모듈을 로드합니다."""
        await ctx.defer()

        try:
            await self.bot.load_extension("musicbot.cogs." + module)
            LOGGER.info(f"로드 성공!\n모듈: {module}")

            embed = discord.Embed(
                title=get_lan(ctx.author.id, "owners_load_success"),
                description=get_lan(ctx.author.id, "owners_module").format(module=module),
                color=self.color
            )

            if f"*~~{module}~~*" in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(f"*~~{module}~~*")] = module
            else:
                EXTENSIONS.append(module)

        except Exception as error:
            LOGGER.error(f"로드 실패!\n에러: {error}")
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "owners_load_fail"),
                description=get_lan(ctx.author.id, "owners_error").format(error=error),
                color=self.error_color
            )

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="reload",
        description="모듈을 리로드합니다."
    )
    @app_commands.describe(
        module="리로드할 모듈을 입력해주세요"
    )
    @commands.is_owner()
    @commands.guild_only()
    @app_commands.guilds(*DEBUG_SERVER)
    async def reload(self, ctx: Context, module):
        """ 모듈을 리로드합니다. """
        try:
            self.bot.reload_extension("musicbot.cogs." + module)
            LOGGER.info(f"리로드 성공!\n모듈: {module}")
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "owners_reload_success"),
                description=get_lan(ctx.author.id, "owners_module").format(module=module),
                color=self.color
            )
        except Exception as error:
            LOGGER.error(f"리로드 실패!\n에러: {error}")
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "owners_reload_fail"),
                description=f'에러: {error}',
                color=self.error_color
            )
            if module in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(module)] = f"*~~{module}~~*"
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="unload",
        description="모듈을 언로드합니다."
    )
    @app_commands.describe(
        module="언로드할 모듈을 입력해주세요"
    )
    @commands.is_owner()
    @commands.guild_only()
    @app_commands.guilds(*DEBUG_SERVER)
    async def unload(self, ctx: Context, module):
        """ 모듈을 언로드합니다. """
        try:
            self.bot.unload_extension("musicbot.cogs." + module)
            LOGGER.info(f"언로드 성공!\n모듈: {module}")
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "owners_unload_success"),
                description=get_lan(ctx.author.id, "owners_module").format(module=module),
                color=self.color
            )
            if module in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(module)] = f"*~~{module}~~*"
        except Exception as error:
            LOGGER.error(f"언로드 실패!\n에러: {error}")
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "owners_unload_fail"),
                description=f'에러: {error}',
                color=self.error_color
            )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="module_list",
        description="모듈을 언로드합니다."
    )
    @commands.is_owner()
    @commands.guild_only()
    @app_commands.guilds(*DEBUG_SERVER)
    async def module_list(self, ctx: Context):
        """ 모든 모듈들의 이름을 알려줘요! """
        modulenum = 0
        for m in EXTENSIONS:
            if not m[0:3] == "*~~":
                modulenum += 1
        modulenum = get_lan(ctx.author.id, 'owners_loaded_modules_len').format(modulenum=modulenum)
        e1 = "\n".join(EXTENSIONS)
        embed = discord.Embed(title=get_lan(ctx.author.id, 'owners_modules_list'), color=COLOR_CODE)
        embed.add_field(name=modulenum, value=e1, inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="serverinfo",
        description="봇 서버의 사양을 알려줘요!"
    )
    @commands.is_owner()
    @commands.guild_only()
    @app_commands.guilds(*DEBUG_SERVER)
    async def serverinfo(self, ctx: Context):
        """ 봇 서버의 사양을 알려줘요! """

        embed = discord.Embed(title=get_lan(ctx.author.id, 'owners_server_info'), color=COLOR_CODE)
        embed.add_field(name="Platform", value=platform.platform(), inline=False)
        embed.add_field(name="Kernel", value=platform.version(), inline=False)
        embed.add_field(name="Architecture", value=platform.machine(), inline=False)
        embed.add_field(name="CPU Usage", value=str(psutil.cpu_percent()) + "%", inline=False)
        memorystr = f"{round((psutil.virtual_memory().used / (1024.0 ** 3)), 1)}GB / {round((psutil.virtual_memory().total / (1024.0 ** 3)), 1)}GB"
        embed.add_field(name="Memory Usage", value=memorystr, inline=False)
        embed.add_field(name="Python Ver",
                        value="%s %s" % (platform.python_implementation(), platform.python_version()), inline=False)
        embed.add_field(name="Py-cord.py Ver", value=str(discord.__version__), inline=False)
        embed.add_field(name="Lavalink.py Ver", value=lavalink.__version__, inline=False)
        embed.add_field(name="Ping", value=str(round(self.bot.latency * 1000)) + "ms", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="server_list",
        description="봇이 들어가있는 모든 서버 리스트를 출력합니다."
    )
    @commands.is_owner()
    @commands.guild_only()
    @app_commands.guilds(*DEBUG_SERVER)
    async def server_list(self, ctx: Context):
        """ 봇이 들어가있는 모든 서버 리스트를 출력합니다. """
        page = 10
        # 페이지 지정값이 없고, 총 서버수가 10 이하일 경우
        if len(self.bot.guilds) <= page:
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "owners_server_list_title").format(BOT_NAME=self.bot.user.name),
                description=get_lan(ctx.author.id, "owners_server_list_description").format(
                    server_count=len(self.bot.guilds),
                    members_count=len(self.bot.users)),
                color=COLOR_CODE
            )
            srvr = str()
            for i in self.bot.guilds:
                srvr = srvr + get_lan(ctx.author.id, "owners_server_list_info").format(
                    server_name=i,
                    server_members_count=i.member_count
                )
            embed.add_field(name="", value=srvr, inline=False)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        # 서버수가 10개 이상일 경우
        # 총 페이지수 계산
        botguild = self.bot.guilds
        # 인원 수 많은 서버부터 표시
        guilds = []
        for guild in botguild:
            guilds.append([guild.name, int(guild.member_count)])
        guilds.sort(key=lambda x: (-x[1], x[0]))

        allpage = math.ceil(len(guilds) / page)

        embeds = []
        for i in range(1, allpage + 1):
            srvr = ""
            numb = (page * i)
            numa = numb - page
            for a in range(numa, numb):
                try:
                    srvr += get_lan(ctx.author.id, "owners_server_list_info").format(
                        server_name=guilds[a][0],
                        server_members_count=guilds[a][1]
                    )
                except IndexError:
                    break

            embed = discord.Embed(
                title=get_lan(ctx.author.id, "owners_server_list_title").format(BOT_NAME=self.bot.user.name),
                description=get_lan(ctx.author.id, "owners_server_list_description2").format(
                    server_count=len(self.bot.guilds),
                    members_count=len(self.bot.users),
                    servers=srvr
                ),
                color=COLOR_CODE
            )
            embed.set_footer(
                text=f"{get_lan(ctx.author.id, 'owners_page')} {str(i)}/{str(allpage)}\n{BOT_NAME_TAG_VER}"
            )
            embeds.append(embed)

        # 커스텀 Paginator 사용
        view = Paginator(embeds=embeds)
        message = await ctx.send(embed=embeds[0], view=view)
        view.message = message  # Set message reference for timeout handling

    @commands.hybrid_command(
        name="public_ip",
        description="서버의 공인 IP를 알려줘요!"
    )
    @commands.is_owner()
    @commands.guild_only()
    @app_commands.guilds(*DEBUG_SERVER)
    async def public_ip(self, ctx: Context):
        """ 서버의 공인 IP를 알려줘요! """
        public_ip = requests.get("https://api.ipify.org").text
        embed = discord.Embed(title="Public IP", color=COLOR_CODE)
        embed.add_field(name="IP", value=public_ip, inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Owners(bot))
    LOGGER.info('Owners Loaded!')
