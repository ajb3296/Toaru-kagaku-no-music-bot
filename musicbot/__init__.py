import os
import sys
import logging

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
    TOKEN            = os.environ.get('TOKEN', None)
    try:
        EXTENSIONS = set(str(x) for x in os.environ.get("EXTENSIONS", 'owners help other ping about music melon').split())
    except ValueError:
        raise Exception("모듈 목록이 올바르지 않습니다.")
    try:
        OWNERS = set(int(x) for x in os.environ.get("OWNERS", "").split())
    except ValueError:
        raise Exception("OWNERS 사용자 목록에 올바른 정수가 없습니다.")
    commandInt       = os.environ.get('commandInt', None)
    BOT_NAME         = os.environ.get('BOT_NAME', None)
    BOT_TAG          = os.environ.get('BOT_TAG', None)
    BOT_VER          = os.environ.get('BOT_VER', None)
    try:
        BOT_ID           = int(os.environ.get('BOT_ID', None))
    except ValueError:
        raise Exception("BOT_ID에 올바른 정수가 없습니다.")
    color_code       = os.environ.get('color_code', None)
    AboutBot         = os.environ.get('AboutBot', None)
    host             = os.environ.get('host', None)
    psw              = os.environ.get('psw', None)
    region           = os.environ.get('region', None)
    name             = os.environ.get('name', None)

else:
    from musicbot.config import Development as Config

    TOKEN            = Config.TOKEN
    EXTENSIONS       = Config.EXTENSIONS
    OWNERS           = Config.OWNERS
    commandInt       = Config.commandInt
    BOT_NAME         = Config.BOT_NAME
    BOT_TAG          = Config.BOT_TAG
    BOT_VER          = Config.BOT_VER
    BOT_ID           = Config.BOT_ID
    color_code       = Config.color_code
    AboutBot         = Config.AboutBot
    host             = Config.host
    psw              = Config.psw
    region           = Config.region
    name             = Config.name

EXTENSIONS = list(EXTENSIONS)

BOT_NAME_TAG_VER = "%s%s | %s" %(BOT_NAME, BOT_TAG, BOT_VER)

f = open("application.yml", 'w')
f.write(f"""server:
  port: 2333
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
