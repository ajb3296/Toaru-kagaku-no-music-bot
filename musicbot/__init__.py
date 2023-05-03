import os
import sys
import logging

from musicbot.utils.make_config import make_config

# Bot version
BOT_VER = "V.3.3"

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("3.6 버전 이상의 Python 이 있어야 합니다. 여러 기능이 해당 Python3.6 버전을 따릅니다. 봇 종료.")
    quit(1)

# Create the config file if it doesn't exist
if not os.path.exists("musicbot/config.py"):
    make_config()
from musicbot.config import Development as Config

TOKEN = Config.TOKEN
OWNERS = Config.OWNERS
DEBUG_SERVER = Config.DEBUG_SERVER
BOT_NAME = Config.BOT_NAME
BOT_TAG = Config.BOT_TAG
BOT_ID = Config.BOT_ID
COLOR_CODE = Config.COLOR_CODE
ABOUT_BOT = Config.ABOUT_BOT
HOST = Config.HOST
PSW = Config.PSW
REGION = Config.REGION
PORT = Config.PORT

KOREANBOT_TOKEN = Config.KOREANBOT_TOKEN
TOPGG_TOKEN = Config.TOPGG_TOKEN

EXTENSIONS = []
for file in os.listdir("musicbot/cogs"):
    if file.endswith(".py"):
        EXTENSIONS.append(file.replace(".py", ""))

BOT_NAME_TAG_VER = "%s%s | %s" % (BOT_NAME, BOT_TAG, BOT_VER)

f = open("application.yml", 'w')
f.write(f"""server:
  port: {PORT}
  address: {HOST}
spring:
  main:
    banner-mode: log
lavalink:
  server:
    password: "{PSW}"
    sources:
      youtube: true
      bandcamp: true
      soundcloud: true
      twitch: true
      vimeo: true
      mixer: true
      http: true
      local: false
    bufferDurationMs: 400
    youtubePlaylistLoadLimit: 6
    playerUpdateInterval: 5
    youtubeSearchEnabled: true
    soundcloudSearchEnabled: true
    gc-warnings: true

metrics:
  prometheus:
    enabled: false
    endpoint: /metrics

sentry:
  dsn: ""
  environment: ""

logging:
  file:
    max-history: 30
    max-size: 1GB
  path: ./logs/

  level:
    root: INFO
    lavalink: INFO""")
f.close()
