import discord
from discord.ext import commands

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code, commandInt, OWNERS, EXTENSIONS

class Help (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (name = 'help', aliases = ['도움', '도움말', '명령어', '헬프'])
    async def help (self, ctx, *, arg : str  = None) :
        if not arg == None:
            arg = arg.upper()
        if arg == "GENERAL" or arg == "일반":
            embed=discord.Embed(title=get_lan(ctx.author.id, "help_general"), description="", color=color_code)

            if "about" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_about_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_general_about_info"), inline=True)

            if "other" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_invite_command").format(commandInt=commandInt),     value=get_lan(ctx.author.id, "help_general_invite_info"), inline=True)
                embed.add_field(name=get_lan(ctx.author.id, "help_general_java_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_general_java_info"), inline=True)
                embed.add_field(name=get_lan(ctx.author.id, "help_general_softver_command").format(commandInt=commandInt),    value=get_lan(ctx.author.id, "help_general_softver_info"), inline=True)
                embed.add_field(name=get_lan(ctx.author.id, "help_general_uptime_command").format(commandInt=commandInt),     value=get_lan(ctx.author.id, "help_general_uptime_info"), inline=True)

            if "ping" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_ping_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_general_ping_info"), inline=True)

            if "neko" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_neko_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_general_neko_info"), inline=True)

            if "translation" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_translation_command").format(commandInt=commandInt),value=get_lan(ctx.author.id, "help_general_translation_info"), inline=True)

            if "set_language" in EXTENSIONS:
                embed.add_field(name=f"`{commandInt}language`", value="Sends a list of available language packs.", inline=True)
                embed.add_field(name=f"`{commandInt}language` [*language pack*]", value="Apply the language pack.", inline=True)

            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

        elif arg == "MUSIC" or arg == "음악":
            if "music" in EXTENSIONS:
                embed=discord.Embed(title=get_lan(ctx.author.id, "help_music"), description=get_lan(ctx.author.id, "help_music_description"), color=color_code)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_connect_command").format(commandInt=commandInt),   value=get_lan(ctx.author.id, "help_music_connect_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_play_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_play_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_stop_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_stop_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_skip_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_skip_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_vol_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_music_vol_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_now_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_music_now_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_q_command").format(commandInt=commandInt),         value=get_lan(ctx.author.id, "help_music_q_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_pause_command").format(commandInt=commandInt),     value=get_lan(ctx.author.id, "help_music_pause_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_shuffle_command").format(commandInt=commandInt),   value=get_lan(ctx.author.id, "help_music_shuffle_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_repeat_command").format(commandInt=commandInt),    value=get_lan(ctx.author.id, "help_music_repeat_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_seek_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_seek_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_remove_command").format(commandInt=commandInt),    value=get_lan(ctx.author.id, "help_music_remove_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_music_find_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_music_find_info").format(commandInt=commandInt), inline=False)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        elif arg == "CHART" or arg == "차트재생" or arg == "차트":
            embed=discord.Embed(title=get_lan(ctx.author.id, "help_play_chart"), description='', color=color_code)
            if "chart" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_general_melon_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_general_melon_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_general_billboard_command").format(commandInt=commandInt),  value=get_lan(ctx.author.id, "help_general_billboard_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_general_billboardjp_command").format(commandInt=commandInt),  value=get_lan(ctx.author.id, "help_general_billboardjp_info"), inline=False)

            if "music" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_play_chart_melonplay_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_play_chart_melonplay_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_play_chart_billboardplay_command").format(commandInt=commandInt),  value=get_lan(ctx.author.id, "help_play_chart_billboardplay_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_play_chart_billboardjpplay_command").format(commandInt=commandInt),  value=get_lan(ctx.author.id, "help_play_chart_billboardjpplay_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_play_chart_listpage_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_play_chart_listpage_info").format(commandInt=commandInt), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_play_chart_listplay_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_play_chart_listplay_info").format(commandInt=commandInt), inline=False)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        elif arg == "DEV" or arg == "개발" or arg == "개발자":
            if ctx.author.id in OWNERS:
                embed=discord.Embed(title=get_lan(ctx.author.id, "help_dev"), description=get_lan(ctx.author.id, "help_dev_description"), color=color_code)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_serverlist_command").format(commandInt=commandInt),   value=get_lan(ctx.author.id, "help_dev_serverlist_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_modules_command").format(commandInt=commandInt),      value=get_lan(ctx.author.id, "help_dev_modules_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_load_command").format(commandInt=commandInt),         value=get_lan(ctx.author.id, "help_dev_load_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_unload_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_dev_unload_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_reload_command").format(commandInt=commandInt),       value=get_lan(ctx.author.id, "help_dev_reload_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_serverinfo_command").format(commandInt=commandInt),   value=get_lan(ctx.author.id, "help_dev_serverinfo_info"), inline=False)
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_broadcast_command").format(commandInt=commandInt),    value=get_lan(ctx.author.id, "help_dev_broadcast_info"), inline=False)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        else:
            embed=discord.Embed(title=get_lan(ctx.author.id, "help"), description=get_lan(ctx.author.id, "help_info").format(bot_name=self.bot.user.name), color=color_code)
            embed.add_field(name=get_lan(ctx.author.id, "help_general_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_general_command_info"), inline=False)

            if "music" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_music_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_music_command_info"), inline=False)

            if "music" in EXTENSIONS:
                embed.add_field(name=get_lan(ctx.author.id, "help_chart_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_chart_command_info"), inline=False)

            if ctx.author.id in OWNERS:
                embed.add_field(name=get_lan(ctx.author.id, "help_dev_command").format(commandInt=commandInt), value=get_lan(ctx.author.id, "help_dev_command_info"), inline=False)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)
            

def setup (bot) :
    bot.add_cog (Help (bot))
    LOGGER.info('Help loaded!')
