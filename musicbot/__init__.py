import os
import sys
import logging

from musicbot.utils.make_config import make_config

# Create the config file if it doesn't exist
if not os.path.exists("musicbot/config.py"):
    make_config()

# Bot version
BOT_VER = "V.3.2"

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error("3.6 버전 이상의 Python 이 있어야 합니다. 여러 기능이 해당 Python3.6 버전을 따릅니다. 봇 종료.")
    quit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)
    try:
        OWNERS = set(int(x) for x in os.environ.get("OWNERS", "").split())
    except ValueError:
        raise Exception("OWNERS 사용자 목록에 올바른 정수가 없습니다.")
    try:
        DebugServer = set(int(x) for x in os.environ.get("DebugServer", "").split())
    except ValueError:
        raise Exception("DebugChannel 사용자 목록에 올바른 정수가 없습니다.")
    BOT_NAME = os.environ.get('BOT_NAME', None)
    BOT_TAG = os.environ.get('BOT_TAG', "#1234")
    try:
        BOT_ID = int(os.environ.get('BOT_ID', None))
    except ValueError:
        raise Exception("BOT_ID에 올바른 정수가 없습니다.")
    color_code = int(os.environ.get('color_code', "0xc68e6e"), 0)
    AboutBot = os.environ.get('AboutBot', None)
    host = os.environ.get('host', "localhost")
    psw = os.environ.get('psw', None)
    region = os.environ.get('region', "en")
    port = int(os.environ.get('port', 2333))

else:
    from musicbot.config import Development as Config

    TOKEN = Config.TOKEN
    OWNERS = Config.OWNERS
    DebugServer = Config.DebugServer
    BOT_NAME = Config.BOT_NAME
    BOT_TAG = Config.BOT_TAG
    BOT_ID = Config.BOT_ID
    color_code = Config.color_code
    AboutBot = Config.AboutBot
    host = Config.host
    psw = Config.psw
    region = Config.region
    port = Config.port

EXTENSIONS = []
for file in os.listdir("musicbot/cogs"):
    if file.endswith(".py"):
        EXTENSIONS.append(file.replace(".py", ""))

BOT_NAME_TAG_VER = "%s%s | %s" %(BOT_NAME, BOT_TAG, BOT_VER)

f = open("application.yml", 'w')
f.write(f"""server:
  port: {port}
  address: {host}
spring:
  main:
    banner-mode: log
lavalink:
  server:
    password: "{psw}"
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
