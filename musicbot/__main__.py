import os
import re
import time
import json
import discord
import asyncio
import requests
import subprocess
import multiprocessing
from urllib import request

from discord.ext import commands

from musicbot.lavalinkstart import start_lavalink
from musicbot.background.db_management import add_today_table

from musicbot import LOGGER, TOKEN, EXTENSIONS, BOT_NAME_TAG_VER

async def status_task():
    while True:
        try:
            await bot.change_presence(
                activity = discord.Game ("/help : 도움말"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
            await bot.change_presence(
                activity = discord.Game (f"{len(bot.guilds)}개의 서버에서 놀고있어요!"),
                status = discord.Status.online,
            )
            await asyncio.sleep(10)
        except Exception:
            pass

class Toaru_kagaku_no_music_bot (commands.Bot) :
    def __init__ (self) :
        super().__init__ (
            intents=intents
        )
        self.remove_command("help")

        # 현재 라바링크 버전
        now_lavalinkver = None
        if os.path.exists("Lavalink.jar"):
            lavalinkver = subprocess.check_output(['java', '-jar', 'Lavalink.jar', '--version'], stderr=subprocess.STDOUT, encoding='utf-8')
            now_lavalinkver = re.search(r"Version:\s+(\d+\.\d+\.\d+)", lavalinkver).group(1)

        # 최신 라바링크 버전
        latest_lavalink_tag = json.loads(requests.get("https://api.github.com/repos/freyacodes/Lavalink/releases").text)[0]['tag_name']

        # 최신 라바링크 버전과 다를 경우
        if now_lavalinkver != latest_lavalink_tag:
            LOGGER.info("Latest Lavalink downloading...")
            LOGGER.info(f"v{now_lavalinkver} -> v{latest_lavalink_tag}")
            lavalink_download_link = f"https://github.com/freyacodes/Lavalink/releases/download/{latest_lavalink_tag}/Lavalink.jar"

            request.urlretrieve(lavalink_download_link, "Lavalink.jar")

        process = multiprocessing.Process(target=start_lavalink)
        process.start()
        time.sleep(20)

        for i in EXTENSIONS :
            self.load_extension("musicbot.cogs." + i)

    async def on_ready (self) :
        LOGGER.info(BOT_NAME_TAG_VER)
        await self.change_presence(
            activity = discord.Game ("/help : 도움말"),
            status = discord.Status.online,
        )
        bot.loop.create_task(status_task())
        bot.loop.create_task(add_today_table())

    async def on_message (self, message) :
        if message.author.bot:
            return
        await self.process_commands (message)


intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = Toaru_kagaku_no_music_bot ()
bot.run(TOKEN)
