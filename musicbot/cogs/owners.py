import discord
import lavalink
from discord.ext import commands
from discord.commands import CommandPermission, SlashCommandGroup
from discord.commands import slash_command
import platform
import psutil

from musicbot.utils.language import get_lan
from musicbot import LOGGER, color_code, BOT_NAME_TAG_VER, EXTENSIONS

class Owners (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot
        self._last_members = None
        self.color = color_code
        self.error_color = 0xff4a4a

    @slash_command(permissions=[CommandPermission("owner", 2, True)], guild_ids=[675171256299028490])
    async def load (self, ctx, module) :
        """ 모듈을 로드합니다. """
        try :
            self.bot.load_extension("musicbot.cogs." + module)
            LOGGER.info(f"로드 성공!\n모듈 : {module}")
            embed = discord.Embed (
                title = get_lan(ctx.author.id, "owners_load_success"),
                description = get_lan(ctx.author.id, "owners_module").format(module=module),
                color = self.color
            )
            if f"*~~{module}~~*" in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(f"*~~{module}~~*")] = module
            else:
                EXTENSIONS.append(module)
        except Exception as error :
            LOGGER.error(f"로드 실패!\n에러 : {error}")
            embed = discord.Embed (
                title = get_lan(ctx.author.id, "owners_load_fail"),
                description = get_lan(ctx.author.id, "owners_error").format(error=error),
                color = self.error_color
            )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed = embed)

    @slash_command(permissions=[CommandPermission("owner", 2, True)], guild_ids=[675171256299028490])
    async def reload (self, ctx, module) :
        """ 모듈을 리로드합니다. """
        try :
            self.bot.reload_extension("musicbot.cogs." + module)
            LOGGER.info(f"리로드 성공!\n모듈 : {module}")
            embed = discord.Embed (
                title = get_lan(ctx.author.id, "owners_reload_success"),
                description = get_lan(ctx.author.id, "owners_module").format(module=module),
                color = self.color
            )
        except Exception as error :
            LOGGER.error(f"리로드 실패!\n에러 : {error}")
            embed = discord.Embed (
                title = get_lan(ctx.author.id, "owners_reload_fail"),
                description = f'에러 : {error}',
                color = self.error_color
            )
            if module in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(module)] = f"*~~{module}~~*"
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed = embed)

    @slash_command(permissions=[CommandPermission("owner", 2, True)], guild_ids=[675171256299028490])
    async def unload (self, ctx, module) :
        """ 모듈을 언로드합니다. """
        try :
            self.bot.unload_extension("musicbot.cogs." + module)
            LOGGER.info(f"언로드 성공!\n모듈 : {module}")
            embed = discord.Embed (
                title = get_lan(ctx.author.id, "owners_unload_success"),
                description = get_lan(ctx.author.id, "owners_module").format(module=module),
                color = self.color
            )
            if module in EXTENSIONS:
                EXTENSIONS[EXTENSIONS.index(module)] = f"*~~{module}~~*"
        except Exception as error :
            LOGGER.error(f"언로드 실패!\n에러 : {error}")
            embed = discord.Embed (
                title = get_lan(ctx.author.id, "owners_unload_fail"),
                description = f'에러 : {error}',
                color = self.error_color
            )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send (embed = embed)

    @slash_command(permissions=[CommandPermission("owner", 2, True)], guild_ids=[675171256299028490])
    async def module_list(self, ctx):
        """ 모든 모듈들의 이름을 알려줘요! """
        modulenum = 0
        for m in EXTENSIONS:
            if not m[0:3] == "*~~":
                modulenum += 1
        modulenum = get_lan(ctx.author.id, 'owners_loaded_modules_len').format(modulenum=modulenum)
        e1 = "\n".join(EXTENSIONS)
        embed=discord.Embed(title=get_lan(ctx.author.id, 'owners_modules_list'), color=color_code)
        embed.add_field(name=modulenum, value=e1, inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

    @slash_command(permissions=[CommandPermission("owner", 2, True)], guild_ids=[675171256299028490])
    async def serverinfo(self, ctx) :
        """ 봇 서버의 사양을 알려줘요! """

        embed=discord.Embed(title=get_lan(ctx.author.id, 'owners_server_info'), color=color_code)
        embed.add_field(name="Platform", value=platform.platform(), inline=False)
        embed.add_field(name="Kernel", value=platform.version(), inline=False)
        embed.add_field(name="Architecture", value=platform.machine(), inline=False)
        embed.add_field(name="CPU Usage", value=str(psutil.cpu_percent()) +"%", inline=False)
        memorystr = str(round((psutil.virtual_memory().used / (1024.0 ** 3)), 1)) + "GB" + " / " + str(round((psutil.virtual_memory().total / (1024.0 ** 3)), 1)) + "GB"
        embed.add_field(name="Memory Usage", value=memorystr, inline=False)
        embed.add_field(name="Python Ver", value=("%s %s") %(platform.python_implementation(), platform.python_version()), inline=False)
        embed.add_field(name="Py-cord.py Ver", value=discord.__version__, inline=False)
        embed.add_field(name="Lavalink.py Ver", value=lavalink.__version__, inline=False)
        embed.add_field(name="Ping", value=str(round(self.bot.latency * 1000)) + "ms", inline=False)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Owners (bot))
    LOGGER.info('Owners Loaded!')
