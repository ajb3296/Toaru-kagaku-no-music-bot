import os
import sqlite3
import discord
from discord.ext import commands
from discord.commands import slash_command

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, color_code

class Language (commands.Cog) :
    def __init__ (self, bot) :
        self.bot = bot

    @slash_command()
    async def language (self, ctx, lang: str = None) :
        """ Apply the language pack. """
        if lang is None:
            files = ""
            for file in os.listdir("musicbot/languages"):
                if file.endswith(".json"):
                    files = files + file.replace(".json", "") + "\n"

            embed=discord.Embed(title=get_lan(ctx.author.id, "set_language_pack_list"), description=files, color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.respond(embed=embed)

        if not os.path.exists(f"musicbot/languages/{lang}.json"):
            embed=discord.Embed(title=get_lan(ctx.author.id, "set_language_pack_not_exist"), color=color_code)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.respond(embed=embed)

        conn = sqlite3.connect("userdata.db", isolation_level=None)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS userdata (id integer PRIMARY KEY, language text)")
        # chack user data
        c.execute("SELECT * FROM userdata WHERE id=:id", {"id": str(ctx.author.id)})
        a = c.fetchone()
        if a is None:
            # add user data
            c.execute(f"INSERT INTO userdata VALUES({ctx.author.id}, '{lang}')")
            embed=discord.Embed(title=get_lan(ctx.author.id, "set_language_complete"), description=f"{lang}", color=color_code)
        else:
            # modify user data
            c.execute("UPDATE userdata SET language=:language WHERE id=:id", {"language": lang, 'id': ctx.author.id})
            embed=discord.Embed(title=get_lan(ctx.author.id, "set_language_complete"), description=f"{a[1]} --> {lang}", color=color_code)
        conn.close()

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot) :
    bot.add_cog (Language (bot))
    LOGGER.info('Language loaded!')
