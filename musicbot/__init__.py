import os
import sys
import pymysql
import logging

from musicbot.utils.make_config import make_config

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
LAVALINK_AUTO_UPDATE = Config.LAVALINK_AUTO_UPDATE
SQL_HOST = Config.SQL_HOST
SQL_USER = Config.SQL_USER
SQL_PASSWORD = Config.SQL_PASSWORD
SQL_DB = Config.SQL_DB

KOREANBOT_TOKEN = Config.KOREANBOT_TOKEN
TOPGG_TOKEN = Config.TOPGG_TOKEN

EXTENSIONS = []
for file in os.listdir("musicbot/cogs"):
    if file.endswith(".py"):
        EXTENSIONS.append(file.replace(".py", ""))

BOT_NAME_TAG_VER = "%s%s | %s" % (BOT_NAME, BOT_TAG, BOT_VER)

f = open("application.yml", 'w')
f.write(f"""server: # REST and WS server
  port: {PORT}
  address: {HOST}
plugins:
#  name: # 플러그인 이름
#    some_key: some_value # 플러그인에 대한 일부 키-값 쌍
#    another_key: another_value
lavalink:
  plugins:
#    - dependency: "group:artifact:version"
#      repository: "repository"
  pluginsDir: "./plugins"
  server:
    password: "{PSW}"
    sources:
      youtube: true
      bandcamp: true
      soundcloud: true
      twitch: true
      vimeo: true
      http: true
      local: false
    filters: # 모든 필터는 기본적으로 활성화되어 있습니다
      volume: true
      equalizer: true
      karaoke: true
      timescale: true
      tremolo: true
      vibrato: true
      distortion: true
      rotation: true
      channelMix: true
      lowPass: true
    bufferDurationMs: 400 # NAS 버퍼의 지속 시간. 값이 높을수록 더 긴 GC 일시 중지에 대해 더 잘 처리됩니다. JDA-NAS를 비활성화하려면 Duration <= 0입니다. 최소 40ms, 값이 낮을수록 일시 중지가 발생할 수 있습니다.
    frameBufferDurationMs: 5000 # 버퍼링할 오디오 시간(밀리초)
    opusEncodingQuality: 10 # Opus 인코더 품질. 유효한 값의 범위는 0에서 10까지입니다. 여기서 10은 최상의 품질이지만 CPU를 가장 많이 사용합니다.
    resamplingQuality: HIGH # 리샘플링 작업의 품질. 유효한 값은 LOW, MEDIUM 및 HIGH입니다. 여기서 HIGH는 CPU를 가장 많이 사용합니다.
    trackStuckThresholdMs: 10000 # 트랙이 멈출 수 있는 시간에 대한 임계값입니다. 오디오 데이터를 반환하지 않으면 트랙이 멈춥니다.
    useSeekGhosting: true # 탐색 고스팅은 탐색이 진행되는 동안 오디오 버퍼가 비워질 때까지 또는 탐색이 준비될 때까지 읽히는 효과입니다.
    youtubePlaylistLoadLimit: 6 # 각 100페이지의 페이지 수
    playerUpdateInterval: 5 # 플레이어 업데이트를 클라이언트에 보내는 빈도(초)
    youtubeSearchEnabled: true
    soundcloudSearchEnabled: true
    gc-warnings: true
    #ratelimit:
      #ipBlocks: ["1.0.0.0/8", "..."] # IP 차단 목록
      #excludedIps: ["...", "..."] # lavalink의 사용에서 명시적으로 제외되어야 하는 ip들
      #strategy: "RotateOnBan" # RotateOnBan | LoadBalance | NanoSwitch | RotatingNanoSwitch
      #searchTriggersFail: true # 429 코드가 발생하는 IP를 실패로 트리거해야 하는지 여부
      #retryLimit: -1 # -1 = 라바플레이어 기본값 | 0 = 무제한 | >0 = 재시도 최대값
    #youtubeConfig: # YouTube의 모든 연령 제한을 피하기 위해 필요하지만 일부 제한된 동영상은 연령 제한 없이도 재생할 수 있습니다.
      #email: "" # 구글 계정 이메일
      #password: "" # 구글 계정 비밀번호
    #httpConfig: # 악의적인 행위자가 음악 노드의 IP를 파악하여 공격하는 것을 차단하는 데 유용합니다. 이렇게 하면 http 프록시만 공격받게 됩니다.
      #proxyHost: "localhost" # 프록시의 호스트네임, (ip 또는 도메인)
      #proxyPort: 3128 # 프록시 포트, 3128 은 squidProxy 의 기본값입니다.
      #proxyUser: "" # 기본 인증 필드에 대한 선택적 사용자, 기본 인증을 사용하지 않는 경우 공백으로 두십시오.
      #proxyPassword: "" # 기본 인증을 위한 비밀번호

metrics:
  prometheus:
    enabled: false
    endpoint: /metrics

sentry:
  dsn: ""
  environment: ""
#  tags:
#    some_key: some_value
#    another_key: another_value

logging:
  file:
    path: ./logs/

  level:
    root: INFO
    lavalink: INFO

  request:
    enabled: true
    includeClientInfo: true
    includeHeaders: true
    includeQueryString: true
    includePayload: true
    maxPayloadLength: 10000


  logback:
    rollingpolicy:
      max-file-size: 1GB
      max-history: 30
""")

f.close()


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