import discord
from discord.ext import commands
from discord.commands import slash_command

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code, AboutBot

class About (commands.Cog) :
    def __init__ (self, bot):
        self.bot = bot

    @slash_command()
    async def about (self, ctx):
        """ Let me tell you about me! """    
        players = 0
        playing_players = 0
        for node in self.bot.lavalink.node_manager.nodes:
            stats = node.stats
            players += stats.players
            playing_players += stats.playing_players

        embed=discord.Embed(title=get_lan(ctx.author.id, "about_bot_info"), description=AboutBot, color=color_code)
        embed.add_field(name=get_lan(ctx.author.id, "about_guild_count"), value=len(self.bot.guilds), inline=True)
        embed.add_field(name=get_lan(ctx.author.id, "about_number_of_music_playback_servers"), value=f"{players}({playing_players} playing)", inline=True)
        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (About (bot))
    LOGGER.info('About loaded!')
