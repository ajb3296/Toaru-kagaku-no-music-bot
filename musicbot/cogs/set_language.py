import os
import pymysql
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext.commands import Context

from musicbot.utils.language import get_lan
from musicbot import LOGGER, BOT_NAME_TAG_VER, COLOR_CODE, SQL_HOST, SQL_USER, SQL_PASSWORD, SQL_DB

lan_pack = []
for file in os.listdir("musicbot/languages"):
    if file.endswith(".json"):
        lan_pack.append(file.replace(".json", ""))


class Language(commands.Cog, name="language"):
    def __init__(self, bot):
        self.bot = bot
        self.userdata_table = "language"

    @commands.hybrid_command(
        name="language",
        description="Apply the language pack."
    )
    @app_commands.describe(
        lang="Choose language pack"
    )
    @app_commands.choices(lang=[
        app_commands.Choice(name=l, value=l) for l in lan_pack
    ])
    async def language(self, ctx: Context, lang: str):
        """ Apply the language pack. """
        if lang is None:
            files = ""
            for file in os.listdir("musicbot/languages"):
                if file.endswith(".json"):
                    files = files + file.replace(".json", "") + "\n"

            embed = discord.Embed(title=get_lan(ctx.author.id, "set_language_pack_list"), description=files, color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        if not os.path.exists(f"musicbot/languages/{lang}.json"):
            embed = discord.Embed(title=get_lan(ctx.author.id, "set_language_pack_not_exist"), color=COLOR_CODE)
            embed.set_footer(text=BOT_NAME_TAG_VER)
            return await ctx.send(embed=embed)

        con = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DB, charset='utf8')
        cur = con.cursor()
        # chack user data
        cur.execute(f"SELECT * FROM {self.userdata_table} WHERE id=%s", (str(ctx.author.id)))
        a = cur.fetchone()
        if a is None:
            # add user data
            cur.execute(f"INSERT INTO {self.userdata_table} VALUES(%s, %s)", (str(ctx.author.id), lang))
            embed = discord.Embed(title=get_lan(ctx.author.id, "set_language_complete"), description=f"{lang}", color=COLOR_CODE)
        else:
            # modify user data
            cur.execute(f"UPDATE {self.userdata_table} SET language=%s WHERE id=%s", (lang, str(ctx.author.id)))
            embed = discord.Embed(title=get_lan(ctx.author.id, "set_language_complete"), description=f"{a[1]} --> {lang}", color=COLOR_CODE)
        con.commit()
        con.close()

        embed.set_footer(text=BOT_NAME_TAG_VER)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Language(bot))
    LOGGER.info('Language loaded!')
