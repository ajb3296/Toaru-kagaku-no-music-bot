import os
import sqlite3
import discord
from discord import option
from discord.ext import commands
from discord.commands import slash_command

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, COLOR_CODE

lan_pack = []
for file in os.listdir("musicbot/languages"):
    if file.endswith(".json"):
        lan_pack.append(file.replace(".json", ""))


class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command()
    @option("lang", description="Choose language pack", choices=lan_pack)
    async def language (self, ctx, lang: str):
        """ Apply the language pack. """
        if lang is None:
            files = ""
            for file in os.listdir("musicbot/languages"):
                if file.endswith(".json"):
                    files = files + file.replace(".json", "") + "\n"

            embed=discord.Embed(title=get_lan(ctx.author.id, "set_language_pack_list"), description=files, color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.respond(embed=embed)

        if not os.path.exists(f"musicbot/languages/{lang}.json"):
            embed=discord.Embed(title=get_lan(ctx.author.id, "set_language_pack_not_exist"), color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.respond(embed=embed)

        con = sqlite3.connect("userdata.db", isolation_level=None)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS userdata (id integer PRIMARY KEY, language text)")
        # chack user data
        cur.execute("SELECT * FROM userdata WHERE id=:id", {"id": str(ctx.author.id)})
        a = cur.fetchone()
        if a is None:
            # add user data
            cur.execute(f"INSERT INTO userdata VALUES({ctx.author.id}, '{lang}')")
            embed=discord.Embed(title=get_lan(ctx.author.id, "set_language_complete"), description=f"{lang}", color=COLOR_CODE)
        else:
            # modify user data
            cur.execute("UPDATE userdata SET language=:language WHERE id=:id", {"language": lang, 'id': ctx.author.id})
            embed=discord.Embed(title=get_lan(ctx.author.id, "set_language_complete"), description=f"{a[1]} --> {lang}", color=COLOR_CODE)
        con.close()

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.respond(embed=embed)

def setup (bot):
    bot.add_cog(Language(bot))
    LOGGER.info('Language loaded!')
