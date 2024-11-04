import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, COLOR_CODE, OWNERS, EXTENSIONS


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="help",
        aliases=['도움', '도움말'],
        description="Send help",
    )
    @app_commands.describe(
        help_option="Choose option"
    )
    @app_commands.choices(help_option=[
        app_commands.Choice(name="INFO", value="INFO"),
        app_commands.Choice(name="GENERAL", value="GENERAL"),
        app_commands.Choice(name="MUSIC", value="MUSIC"),
        app_commands.Choice(name="CHART", value="CHART")
    ])
    async def help(self, ctx: Context, *, help_option = None):
        """ Send help """
        if help_option is not None:
            help_option = help_option.upper()
        if help_option == "GENERAL" or help_option == "일반":
            embed = discord.Embed(title=get_lan(ctx.author.id, "help_general"), description="", color=COLOR_CODE)

            if "about" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_general_about_command"),
                    value=get_lan(ctx.author.id, "help_general_about_info"),
                    inline=True
                )

            if "other" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_general_invite_command"),
                    value=get_lan(ctx.author.id, "help_general_invite_info"),
                    inline=True
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_general_java_command"),
                    value=get_lan(ctx.author.id, "help_general_java_info"),
                    inline=True
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_general_softver_command"),
                    value=get_lan(ctx.author.id, "help_general_softver_info"),
                    inline=True
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_general_uptime_command"),
                    value=get_lan(ctx.author.id, "help_general_uptime_info"),
                    inline=True
                )

            if "ping" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_general_ping_command"),
                    value=get_lan(ctx.author.id, "help_general_ping_info"),
                    inline=True
                )

            if "set_language" in EXTENSIONS:
                embed.add_field(
                    name="`/language`",
                    value="Sends a list of available language packs.",
                    inline=True
                )
                embed.add_field(
                    name="`/language` [*language pack*]",
                    value="Apply the language pack.",
                    inline=True
                )

            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

        elif help_option == "MUSIC" or help_option == "음악":
            if "music" in EXTENSIONS:
                embed = discord.Embed(
                    title=get_lan(ctx.author.id, "help_music"),
                    description=get_lan(ctx.author.id, "help_music_description"),
                    color=COLOR_CODE
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_connect_command"),
                    value=get_lan(ctx.author.id, "help_music_connect_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_play_command"),
                    value=get_lan(ctx.author.id, "help_music_play_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_stop_command"),
                    value=get_lan(ctx.author.id, "help_music_stop_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_skip_command"),
                    value=get_lan(ctx.author.id, "help_music_skip_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_vol_command"),
                    value=get_lan(ctx.author.id, "help_music_vol_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_now_command"),
                    value=get_lan(ctx.author.id, "help_music_now_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_q_command"),
                    value=get_lan(ctx.author.id, "help_music_q_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_pause_command"),
                    value=get_lan(ctx.author.id, "help_music_pause_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_shuffle_command"),
                    value=get_lan(ctx.author.id, "help_music_shuffle_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_repeat_command"),
                    value=get_lan(ctx.author.id, "help_music_repeat_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_seek_command"),
                    value=get_lan(ctx.author.id, "help_music_seek_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_remove_command"),
                    value=get_lan(ctx.author.id, "help_music_remove_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_equalizer_command"),
                    value=get_lan(ctx.author.id, "help_music_equalizer_info"),
                    inline=False
                )
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        elif help_option == "CHART" or help_option == "차트재생" or help_option == "차트":
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "help_chart"),
                description='',
                color=COLOR_CODE
            )
            if "chart" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_chart_chart_command"),
                    value=get_lan(ctx.author.id, "help_chart_chart_info"),
                    inline=False
                )
            if "music" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_chart_chartplay_command"),
                    value=get_lan(ctx.author.id, "help_chart_chartplay_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_chart_listpage_command"),
                    value=get_lan(ctx.author.id, "help_chart_listpage_info"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_chart_listplay_command"),
                    value=get_lan(ctx.author.id, "help_chart_listplay_info"),
                    inline=False
                )
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "help"),
                description=get_lan(ctx.author.id, "help_info").format(bot_name=self.bot.user.name),
                color=COLOR_CODE
            )
            embed.add_field(
                name=get_lan(ctx.author.id, "help_general_command"),
                value=get_lan(ctx.author.id, "help_general_command_info"),
                inline=False
            )

            if "music" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_music_command"),
                    value=get_lan(ctx.author.id, "help_music_command_info"),
                    inline=False
                )

            if "music" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_chart_command"),
                    value=get_lan(ctx.author.id, "help_chart_command_info"),
                    inline=False
                )

            if ctx.author.id in OWNERS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "help_dev_command"),
                    value=get_lan(ctx.author.id, "help_dev_command_info"),
                    inline=False
                )
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
    LOGGER.info('Help loaded!')
