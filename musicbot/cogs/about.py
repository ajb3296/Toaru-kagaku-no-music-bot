import discord
import asyncio
from discord.ext import commands
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code, commandInt, BOT_NAME, OWNERS, AboutBot

class About (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @commands.command (aliases = ['봇', '개발자', '봇정보', '봇관련', '관련', '정보'])
    async def about (self, ctx) :
        embed=discord.Embed(title="**봇에 대한 정보**", description=f"{AboutBot}\n\n이 봇의 출처는 [이곳](<https://github.com/NewPremium/Toaru-kagaku-no-music-bot>) 입니다.\n또한 [GPL v3.0](<https://www.gnu.org/licenses/gpl-3.0.html>) 이 적용되어 있습니다.", color=color_code)
        embed.add_field(name="서버수", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="유저수", value=len(self.bot.users), inline=True)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)
        
def setup (bot) :
    bot.add_cog (About (bot))
    LOGGER.info('About loaded!')
