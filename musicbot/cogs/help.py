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
            embed = discord.Embed(title=get_lan(ctx.author.id, "**기본적인 명령어**"), description="", color=COLOR_CODE)

            if "about" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/about`"),
                    value=get_lan(ctx.author.id, "저에 대한 정보를 알려드려요!"),
                    inline=True
                )

            if "other" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/invite`"),
                    value=get_lan(ctx.author.id, "저랑 다른 서버에서 놀고싶으세요? 당신이 서버의 관리자라면 저를 서버에 초대할 수 있어요!"),
                    inline=True
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/java`"),
                    value=get_lan(ctx.author.id, "서버에 설치된 자바 버전을 알려드려요!"),
                    inline=True
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/softver`"),
                    value=get_lan(ctx.author.id, "관련 모듈 버전을 알려드려요!"),
                    inline=True
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/uptime`"),
                    value=get_lan(ctx.author.id, "서버가 부팅으로부터 얼마나 지났는지를 알려드려요!"),
                    inline=True
                )

            if "ping" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/ping`"),
                    value=get_lan(ctx.author.id, "핑 속도를 측정해요!"),
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
                    title=get_lan(ctx.author.id, "**음악 명령어**"),
                    description=get_lan(ctx.author.id, "소괄호 () 은(는) 옵션인 경우 쓰입니다. 명령어 뒷쪽의 모든 괄호는 빼주세요!"),
                    color=COLOR_CODE
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":white_check_mark: | `/connect`"),
                    value=get_lan(ctx.author.id, ">>> 음성 채널에 접속해요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":arrow_forward: | `/play` [*음악 이름 혹은 링크*]"),
                    value=get_lan(ctx.author.id, ">>> 음악을 재생해요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":x: | `/disconnect`"),
                    value=get_lan(ctx.author.id, ">>> 음성 채널을 나갑니다."),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":track_next: | `/skip`"),
                    value=get_lan(ctx.author.id, ">>> 다음 곡으로 넘어갑니다!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":loud_sound: | `/volume` (*1~1000*)"),
                    value=get_lan(ctx.author.id, ">>> 음량을 조절합니다!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":arrow_down_small: | `/nowplaying`"),
                    value=get_lan(ctx.author.id, ">>> 현재 재생중인 곡을 알려드려요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":regional_indicator_q: | `/queue`"),
                    value=get_lan(ctx.author.id, ">>> 재생 대기목록을 알려드려요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":play_pause: | `/pause`"),
                    value=get_lan(ctx.author.id, ">>> 음악을 일시정지하거나 재개해요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":twisted_rightwards_arrows: | `/shuffle`"),
                    value=get_lan(ctx.author.id, ">>> 다음 곡부터 재생목록의 음악들이 랜덤으로 나와요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":repeat: | `/repeat`"),
                    value=get_lan(ctx.author.id, ">>> 모든 곡 혹은 한 곡을 반복해서 들려드려요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":clock: | `/seek` [*+(초) 혹은 -(초)*]"),
                    value=get_lan(ctx.author.id, ">>> 음악을 명령어 뒤의 숫자만큼 초단위로 진행시간을 조절해요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":asterisk: | `/remove` [*재생목록에서의 음악 순서 번호*]"),
                    value=get_lan(ctx.author.id, ">>> 재생목록에서 음악을 제거해요!"),
                    inline=False
                )
                embed.add_field(
                    name=get_lan(ctx.author.id, ":control_knobs: | `/equalizer`"),
                    value=get_lan(ctx.author.id, "이퀄라이저 설정을 위한 대시보드를 보내드려요!"),
                    inline=False
                )
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        elif help_option == "CHART" or help_option == "차트재생" or help_option == "차트":
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "**차트 재생 명령어**"),
                description='',
                color=COLOR_CODE
            )
            if "chart" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, ":page_with_curl: | `/chart` [*차트 사이트*]"),
                    value=get_lan(ctx.author.id, ">>> 선택하신 차트사이트에서 1위부터 10위까지 알려드려요!"),
                    inline=False
                )
            if "music" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, ":arrow_forward: | `/chartplay` [*차트 사이트*] [재생할 음악 개수]"),
                    value=get_lan(ctx.author.id, ">>> 선택하신 차트사이트에서 1위에서 [재생할 음악 개수]위 까지의 곡을 재생목록에 추가합니다! [재생할 음악 개수]의 기본값은 10 입니다!"),
                    inline=False
                )
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title=get_lan(ctx.author.id, "**도움말**"),
                description=get_lan(ctx.author.id, "안녕하세요! 전 {bot_name} 에요! 아래에 있는 명령어들을 이용해 도움말을 보세요!").format(bot_name=self.bot.user.name),
                color=COLOR_CODE
            )
            embed.add_field(
                name=get_lan(ctx.author.id, "`/help GENERAL`"),
                value=get_lan(ctx.author.id, ">>> 기본적인 명령어들을 보내드려요!"),
                inline=False
            )

            if "music" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/help MUSIC`"),
                    value=get_lan(ctx.author.id, ">>> 음악 관련 명령어들을 보내드려요!"),
                    inline=False
                )

            if "music" in EXTENSIONS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/help CHART`"),
                    value=get_lan(ctx.author.id, ">>> 음악 차트 관련 명령어들을 보내드려요!"),
                    inline=False
                )

            if ctx.author.id in OWNERS:
                embed.add_field(
                    name=get_lan(ctx.author.id, "`/dev_help`"),
                    value=get_lan(ctx.author.id, ">>> 개발자님이 사용가능한 명령어들을 보내드려요!"),
                    inline=False
                )
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
    LOGGER.info('Help loaded!')
