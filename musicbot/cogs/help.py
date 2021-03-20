import discord
from discord.ext import commands
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code, commandInt, OWNERS, EXTENSIONS

class Help (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (name = 'help', aliases = ['도움', '도움말', '명령어', '헬프', '?'])
    async def help (self, ctx, *, arg : str  = None) :
        if not arg == None:
            arg = arg.upper()
        if arg == "GENERAL" or arg == "일반":
            embed=discord.Embed(title="**기본적인 명령어**", description='명령어 뒷쪽의 모든 괄호는 빼주세요!', color=color_code)

            if "about" in EXTENSIONS:
                embed.add_field(name=f"`{commandInt}about`",   value="저에 대한 정보를 알려드려요!", inline=True)

            if "other" in EXTENSIONS:
                embed.add_field(name=f"`{commandInt}초대`",     value="저랑 다른 서버에서 놀고싶으세요? 당신이 서버의 관리자라면 저를 서버에 초대할 수 있어요!", inline=True)
                embed.add_field(name=f"`{commandInt}java`",    value="서버에 설치된 자바 버전을 알려드려요!", inline=True)
                embed.add_field(name=f"`{commandInt}uptime`",  value="서버가 부팅으로부터 얼마나 지났는지를 알려드려요!", inline=True)

            if "ping" in EXTENSIONS:
                embed.add_field(name=f"`{commandInt}ping`",     value="핑 속도를 측정해요!", inline=True)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

        elif arg == "MUSIC" or arg == "음악":
            if "music" in EXTENSIONS:
                embed=discord.Embed(title="**음악 명령어**", description='소괄호 () 은(는) 옵션인 경우 쓰입니다. 명령어 뒷쪽의 모든 괄호는 빼주세요!', color=color_code)
                embed.add_field(name=f":white_check_mark: | `{commandInt}connect`",                      value=f">>> 음성 채널에 접속해요!\n`{commandInt}join`, `{commandInt}c`, `{commandInt}들어와`, `{commandInt}ㅊ` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":arrow_forward: | `{commandInt}play` [*음악 이름 혹은 Youtube 링크*]", value=f">>> 음악을 재생해요!\n`{commandInt}p`, `{commandInt}재생`, `{commandInt}ㅔ`  을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":x: | `{commandInt}disconnect`",                                  value=f">>> 음성 채널을 나갑니다.\n`{commandInt}dc`, `{commandInt}연결해제`, `{commandInt}나가` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":track_next: | `{commandInt}skip` (*뛰어넘을 곡 수*)",               value=f">>> 다음 곡으로 넘어갑니다!\n(뛰어넘을 곡 수)에 숫자를 입력하시면 그 숫자만큼 곡을 건너뛰어요!\n`{commandInt}스킵`, `{commandInt}s`, `{commandInt}ㄴ` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":loud_sound: | `{commandInt}vol` *(1~1000)*",                     value=f">>> 음량을 조절합니다!\n`{commandInt}v`, `{commandInt}ㅍ`, `{commandInt}음량`, `{commandInt}볼륨` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":arrow_down_small: | `{commandInt}now`",                          value=f">>> 현재 재생중인 곡을 알려드려요!\n`{commandInt}n`, `{commandInt}np`, `{commandInt}현재재생중`, `{commandInt}ㅜ` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":regional_indicator_q: | `{commandInt}q` *(페이지 수)*",            value=f">>> 재생목록 리스트의 *(페이지 수)*의 페이지에 있는 재생목록을 알려드려요!\n`{commandInt}큐`, `{commandInt}ㅂ` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":play_pause: | `{commandInt}pause`",                              value=f">>> 음악을 일시정지해요!\n`{commandInt}일시정지` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":twisted_rightwards_arrows: | `{commandInt}shuffle`",             value=f">>> 다음 곡부터 재생목록의 음악들이 랜덤으로 나와요\n`{commandInt}셔플` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":repeat: | `{commandInt}repeat`",                                 value=f">>> 현재 듣고 계시는 노래를 포함한 재생목록의 모든 노래를 반복해서 들려드려요!\n`{commandInt}loop`,`{commandInt}l`, `{commandInt}반복`, `{commandInt}ㅣ` 을(를) 사용할 수도 있어요." , inline=False)
                embed.add_field(name=f":stop_button: | `{commandInt}stop` *(분)*",                        value=f">>> 듣고 계시는 음악을 끄고 재생목록을 제거해요!\n분 에 분단위 시간을 넣으시면 해당 분 후 음악이 자동으로 멈춥니다!\n`{commandInt}중지`, `{commandInt}정지` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":clock: | `{commandInt}seek` [*+(초) 혹은 -(초)*]",                 value=f">>> 음악을 명령어 뒤의 숫자만큼 초단위로 진행시간을 조절해요!\n`{commandInt}탐색` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":asterisk: | `{commandInt}remove` [*재생목록에서의 음악 순서 번호*]",    value=f">>> 재생목록에서 음악을 제거해요!\n`{commandInt}제거`, `{commandInt}rm` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":globe_with_meridians: | `{commandInt}find` [*검색하실 음악명*]",     value=f">>> Youtube 에서 음악을 검색하고 결과를 알려드려요!\n`{commandInt}youtube`, `{commandInt}유튜브` 을(를) 사용할 수도 있어요.", inline=False)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        elif arg == "CHART" or arg == "차트재생" or arg == "차트":
            if "music" in EXTENSIONS:
                embed=discord.Embed(title="**차트 재생 명령어**", description='', color=color_code)
                embed.add_field(name=f":melon: | `{commandInt}melonplay` (~위까지)",                               value=f">>> 멜론 차트 원하는 순위까지의 곡을 재생목록에 추가합니다!(최대 10위)\n`{commandInt}aw`, `{commandInt}멜론재생`, `{commandInt}멜론음악`, `{commandInt}멜론차트재생` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":b: | `{commandInt}billboardplay` (~위까지)",                               value=f">>> 빌보드 차트 원하는 순위까지의 곡을 재생목록에 추가합니다!(최대 10위)\n`{commandInt}qw`, `{commandInt}빌보드재생`, `{commandInt}빌보드음악`, `{commandInt}빌보드차트재생` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":page_with_curl: | `{commandInt}list` (페이지 수)",                         value=f">>> 재생목록들을 불러와요!\n`{commandInt}리스트`, `{commandInt}재생목록` 을(를) 사용할 수도 있어요.", inline=False)
                embed.add_field(name=f":page_with_curl: | `{commandInt}list` (재생목록 이름)",                     value=f">>> 해당 재생목록의 음악들을 재생해요!\n애니메이션 OP/ED 가 중점으로 추가돼있어요!\n`{commandInt}리스트`, `{commandInt}재생목록` 을(를) 사용할 수도 있어요.", inline=False)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        elif arg == "DEV" or arg == "개발" or arg == "개발자":
            if ctx.author.id in OWNERS:
                embed=discord.Embed(title="**개발자 명령어**", description='명령어 뒷쪽의 모든 괄호는 빼주세요!', color=color_code)
                embed.add_field(name=f"`{commandInt}서버목록` [*페이지수*]",          value=">>> 제가 들어가 있는 서버 정보를 알려줘요.\n페이지당 10개를 표시해요,", inline=False)
                embed.add_field(name=f"`{commandInt}modules`",                   value=">>> 모든 모듈의 이름을 알려줘요!", inline=False)
                embed.add_field(name=f"`{commandInt}load` [*모듈명*]",             value=">>> 모듈을 로드해요!", inline=False)
                embed.add_field(name=f"`{commandInt}unload` [*모듈명*]",           value=">>> 모듈을 언로드해요!", inline=False)
                embed.add_field(name=f"`{commandInt}reload` [*모듈명*]",           value=">>> 모듈을 리로드해요!", inline=False)
                embed.add_field(name=f"`{commandInt}serverinfo`",                 value=">>> 봇 서버의 사양을 알려줘요!", inline=False)
                embed.add_field(name=f"`{commandInt}broadcast` [*공지 내용*]",      value=">>> 공지를 모든 서버에 전송해요!", inline=False)
                embed.set_footer(text=BOT_NAME_TAG_VER)
                await ctx.send(embed=embed)

        else:
            embed=discord.Embed(title="**도움말**", description=f'안녕하세요! 전 {self.bot.user.name} 에요! 아래에 있는 명령어들을 이용해 도움말을 보세요!', color=color_code)
            embed.add_field(name=f"`{commandInt}help general`", value=">>> 기본적인 명령어들을 보내드려요!", inline=False)

            if "music" in EXTENSIONS:
                embed.add_field(name=f"`{commandInt}help music`", value=">>> 음악 관련 명령어들을 보내드려요!", inline=False)

            if "music" in EXTENSIONS:
                embed.add_field(name=f"`{commandInt}help chart`", value=">>> 음악 차트 재생 관련 명령어들을 보내드려요!", inline=False)

            if ctx.author.id in OWNERS:
                embed.add_field(name=f"`{commandInt}help dev`", value=">>> 개발자님이 사용가능한 명령어들을 보내드려요!", inline=False)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            await ctx.send(embed=embed)

def setup (bot) :
    bot.add_cog (Help (bot))
    LOGGER.info('Help loaded!')
