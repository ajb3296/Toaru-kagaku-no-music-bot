import os
import time
import discord
import asyncio
import multiprocessing

import topgg
from koreanbots.integrations.discord import DiscordpyKoreanbots

from discord.ext import commands

from musicbot.lavalinkstart import start_lavalink, download_lavalink
from musicbot.background.db_management import add_today_table
from musicbot.utils.environment_variable import EnV

from musicbot import LOGGER, TOKEN, EXTENSIONS, BOT_NAME_TAG_VER, koreanbot_token, topgg_token

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

        # 환경변수 설정
        EnV().set_bot_env()

        # 라바링크 업데이트 확인 및 다운로드
        download_lavalink()

        LOGGER.info("Lavalink starting...")
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
if koreanbot_token is not None:
    kb = DiscordpyKoreanbots(bot, koreanbot_token, run_task=True)
if topgg_token is not None:
    topgg.DBLClient(bot, topgg_token, autopost=True, post_shard_count=True)
bot.run(TOKEN)