import time
import discord
import asyncio
import multiprocessing

import topgg
from koreanbots.integrations.discord import DiscordpyKoreanbots

from discord.ext import commands, tasks

from musicbot.lavalinkstart import start_lavalink, download_lavalink
# from musicbot.background.update_cache import update_cache_process

from musicbot import LOGGER, TOKEN, OWNERS, EXTENSIONS, BOT_NAME_TAG_VER, KOREANBOT_TOKEN, TOPGG_TOKEN, LAVALINK_AUTO_UPDATE, START_WITH_LAVALINK

class ToaruKagakuNoMusicBot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=intents,
            command_prefix=commands.when_mentioned_or("?"),
            description="간편한 음악 봇",
            help_command=None,
            owner_ids=set(OWNERS),
        )

        # 라바링크 시작
        if START_WITH_LAVALINK:
            # 라바링크 업데이트 확인 및 다운로드
            if LAVALINK_AUTO_UPDATE:
                download_lavalink()

            LOGGER.info("Lavalink starting...")
            process = multiprocessing.Process(target=start_lavalink)
            process.start()
            time.sleep(20)

    @tasks.loop(seconds=20)
    async def status_task(self) -> None:
        try:
            await bot.change_presence(
                activity=discord.Game("/help : 도움말"),
                status=discord.Status.online,
            )
            await asyncio.sleep(10)
            await bot.change_presence(
                activity=discord.Game(f"{len(bot.guilds)}개의 서버에서 놀고있어요!"),
                status=discord.Status.online,
            )
        except Exception:
            pass

    @status_task.before_loop
    async def before_status_task(self) -> None:
        await self.wait_until_ready()

    async def setup_hook(self):
        LOGGER.info(BOT_NAME_TAG_VER)

        for i in EXTENSIONS:
            await self.load_extension("musicbot.cogs." + i)

        await self.tree.sync()
        
        self.status_task.start()
    
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        await self.process_commands(message)

intents = discord.Intents.default()
# intents.message_content = True
intents.guilds = True

bot = ToaruKagakuNoMusicBot()
if KOREANBOT_TOKEN is not None:
    kb = DiscordpyKoreanbots(bot, KOREANBOT_TOKEN, run_task=True)
if TOPGG_TOKEN is not None:
    topgg.DBLClient(bot, TOPGG_TOKEN, autopost=True, post_shard_count=True)
bot.run(TOKEN)
