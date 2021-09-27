import time
import json
import discord
import asyncio
import requests
import multiprocessing
from urllib import request
from discord.ext import commands

from musicbot.lavalinkstart import child_process
from musicbot import LOGGER, TOKEN, EXTENSIONS, commandInt, BOT_NAME_TAG_VER

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
        except Exception:
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
        a = requests.get("https://api.github.com/repos/Cog-Creators/Lavalink-Jars/releases")
        b = json.loads(a.text)
        request.urlretrieve(f"https://github.com/Cog-Creators/Lavalink-Jars/releases/download/{b[0]['tag_name']}/Lavalink.jar", "Lavalink.jar")

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
        if message.author.bot:
            return
        await self.process_commands (message)

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = Toaru_kagaku_no_music_bot ()
bot.run (TOKEN, bot=True)
