import discord
import asyncio
import logging
import sys
import time
import os
from urllib import request
import multiprocessing
from musicbot.lavalinkstart import child_process
from discord.ext import commands
from musicbot.utils import *

from musicbot import LOGGER, TOKEN, EXTENSIONS, OWNERS, commandInt, BOT_NAME, BOT_TAG, BOT_VER, BOT_ID, BOT_NAME_TAG_VER, color_code

async def status_task():
    while True:
        try:
            await bot.change_presence(
                activity = discord.Game (f"{commandInt}help : 도움말"),
                status = discord.Status.online,
                afk = False
            )
            await asyncio.sleep(10)
            await bot.change_presence(
                activity = discord.Game ("%d개의 서버에서 놀고있어요!" %len(bot.guilds)),
                status = discord.Status.online,
                afk = False
            )
            await asyncio.sleep(10)
            await bot.change_presence(
                activity = discord.Game ("%d명의 유저들과 놀고있어요!" %len(bot.users)),
                status = discord.Status.online,
                afk = False
            )
            await asyncio.sleep(10)
        except:
            pass

class Toaru_kagaku_no_music_bot (commands.Bot) :
    def __init__ (self) :

        super().__init__ (
            command_prefix=commandInt,
            intents=intents
        )
        self.remove_command("help")

        # Lavalink Download

        LOGGER.info("Lavalink Downloading...")
        request.urlretrieve(f"https://github.com/Cog-Creators/Lavalink-Jars/releases/latest/download/Lavalink.jar", "Lavalink.jar")

        process = multiprocessing.Process(target=child_process)
        process.start()
        time.sleep(20)

        for i in EXTENSIONS :
            self.load_extension ("musicbot.cogs." + i)

    async def on_ready (self) :
        LOGGER.info(BOT_NAME_TAG_VER)
        await self.change_presence(
            activity = discord.Game (f"{commandInt}help : 도움말"),
            status = discord.Status.online,
            afk = False
        )
        bot.loop.create_task(status_task())
    
    async def on_message (self, message) :
        if message.author.bot :
            return
        else :
            await self.process_commands (message)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = Toaru_kagaku_no_music_bot ()
bot.run (TOKEN, bot=True)
