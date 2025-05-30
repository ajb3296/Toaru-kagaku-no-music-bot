import os
import sys
import json
import pymysql
import logging

from musicbot.utils.make_config import make_config
from musicbot.utils.make_application_yml import make_application_yml

# Bot version
BOT_VER = "V.3.5"

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.10, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 10:
    LOGGER.error("3.10 버전 이상의 Python 이 있어야 합니다. 여러 기능이 Python3.10 버전을 따릅니다. 봇 종료.")
    quit(1)


ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', "")
    OWNERS = list(map(int, os.environ.get('OWNERS', "").split(',')))
    DEBUG_SERVER = list(map(int, os.environ.get('DEBUG_SERVER', "").split(',')))
    BOT_NAME = os.environ.get('BOT_NAME', "")
    BOT_TAG = os.environ.get('BOT_TAG', "#")
    BOT_ID = int(os.environ.get('BOT_ID', 0))
    COLOR_CODE = int(os.environ.get('COLOR_CODE', '0x2F3136'), 16)
    ABOUT_BOT = os.environ.get('ABOUT_BOT', "")
    START_WITH_LAVALINK = bool(os.environ.get('START_WITH_LAVALINK', True))

    HOST = os.environ.get('HOST', 'localhost')
    PSW = os.environ.get('PSW', 'tkbot_since_20200525')
    REGION = os.environ.get('REGION', 'US')
    PORT = int(os.environ.get('PORT', 2333))
    LAVALINK_AUTO_UPDATE = bool(os.environ.get('LAVALINK_AUTO_UPDATE', True))
    LAVALINK_PLUGINS = json.loads(os.environ.get('LAVALINK_PLUGINS', """
        {
            "dev.lavalink.youtube:youtube-plugin": "https://api.github.com/repos/lavalink-devs/youtube-source/releases"
        }
    """))
    SQL_HOST = os.environ.get('SQL_HOST', 'localhost')
    SQL_USER = os.environ.get('SQL_USER', 'tkbot')
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD', 'tkbot_since_20200525')
    SQL_DB = os.environ.get('SQL_DB', 'tkbot')
    USING_IPV6_TUNNELING = bool(os.environ.get('USING_IPV6_TUNNELING', False))
    IP_BLOCKS = os.environ.get('IP_BLOCKS', '').split(',')
    EXCLUDE_IPS = os.environ.get('EXCLUDE_IPS', '').split(',')
    STRATEGY = os.environ.get('STRATEGY', 'RotateOnBan')

    KOREANBOT_TOKEN = os.environ.get('KOREANBOT_TOKEN', None)
    TOPGG_TOKEN = os.environ.get('TOPGG_TOKEN', None)


else:
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
    START_WITH_LAVALINK = Config.START_WITH_LAVALINK
    HOST = Config.HOST
    PSW = Config.PSW
    REGION = Config.REGION
    PORT = Config.PORT
    LAVALINK_AUTO_UPDATE = Config.LAVALINK_AUTO_UPDATE
    LAVALINK_PLUGINS = Config.LAVALINK_PLUGINS
    SQL_HOST = Config.SQL_HOST
    SQL_USER = Config.SQL_USER
    SQL_PASSWORD = Config.SQL_PASSWORD
    SQL_DB = Config.SQL_DB
    USING_IPV6_TUNNELING = Config.USING_IPV6_TUNNELING
    IP_BLOCKS = Config.IP_BLOCKS
    EXCLUDE_IPS = Config.EXCLUDE_IPS
    STRATEGY = Config.STRATEGY


    KOREANBOT_TOKEN = Config.KOREANBOT_TOKEN
    TOPGG_TOKEN = Config.TOPGG_TOKEN

EXTENSIONS = []
for file in os.listdir("musicbot/cogs"):
    if file.endswith(".py"):
        EXTENSIONS.append(file.replace(".py", ""))

BOT_NAME_TAG_VER = "%s%s | %s" % (BOT_NAME, BOT_TAG, BOT_VER)


make_application_yml(HOST, PORT, PSW, LOGGER, LAVALINK_PLUGINS, USING_IPV6_TUNNELING, IP_BLOCKS, EXCLUDE_IPS, STRATEGY)


# DB 생성
con = pymysql.connect(host = SQL_HOST,
                       user = SQL_USER,
                       password = SQL_PASSWORD,
                       charset = 'utf8')
cur = con.cursor()

cur.execute("CREATE DATABASE IF NOT EXISTS tkbot")

con.commit()
con.close()

con = pymysql.connect(host = SQL_HOST,
                        user = SQL_USER,
                        password = SQL_PASSWORD,
                        db = SQL_DB,
                        charset = 'utf8')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS statistics (date date, video_id text, count int)")
cur.execute("CREATE TABLE IF NOT EXISTS language (id text, language text)")
cur.execute("CREATE TABLE IF NOT EXISTS loop_setting (guild_id text, loop_set int)")
cur.execute("CREATE TABLE IF NOT EXISTS shuffle (guild_id text, shuffle bool)")

con.commit()
con.close()
