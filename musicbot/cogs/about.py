import discord
from discord.ext import commands
from discord.ext.commands import Context

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, COLOR_CODE, ABOUT_BOT


class About(commands.Cog, name="about"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="about",
        description="Let me tell you about me!",
    )
    async def about(self, ctx: Context):
        """ Let me tell you about me! """
        player_server_count = 0
        for i in self.bot.guilds:
            player = self.bot.lavalink.player_manager.get(int(i.id))
            try:
                if player.is_connected:
                    player_server_count += 1
            except Exception:
                pass

        players = 0
        playing_players = 0
        for node in self.bot.lavalink.node_manager.nodes:
            stats = node.stats
            players += stats.players
            playing_players += stats.playing_players

        embed = discord.Embed(title=get_lan(ctx.author.id, "**봇에 대한 정보**"), description=ABOUT_BOT, color=COLOR_CODE)
        embed.add_field(
            name="Github",
            value="[Toaru-kagaku-no-music-bot](https://github.com/ajb3296/Toaru-kagaku-no-music-bot)",
            inline=False
        )
        embed.add_field(
            name=get_lan(ctx.author.id, "서버 수"),
            value=str(len(self.bot.guilds)),
            inline=True
        )
        embed.add_field(
            name=get_lan(ctx.author.id, "음악 재생 서버 수"),
            value=f"lavalink: {players}({playing_players} playing)\nvoice channel count: {player_server_count} playing",
            inline=True
        )
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(About(bot))
    LOGGER.info("About loaded!")