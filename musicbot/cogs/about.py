import discord
from discord.ext import commands
from discord.commands import slash_command

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code, AboutBot

class About (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def about (self, ctx) :
        """ Let me tell you about me! """
        player_server_count=0
        for i in self.bot.guilds:
            player = self.bot.lavalink.player_manager.get(int(i.id))
            try:
                if player.is_connected:
                    player_server_count += 1
            except Exception:
                pass
        embed=discord.Embed(title=get_lan(ctx.author.id, "about_bot_info"), description=AboutBot, color=color_code)
        embed.add_field(name=get_lan(ctx.author.id, "about_guild_count"), value=len(self.bot.guilds), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "about_number_of_music_playback_servers"), value=player_server_count, inline=True)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (About (bot))
    LOGGER.info('About loaded!')
