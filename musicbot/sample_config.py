if not __name__.endswith("sample_config"):
    import sys

    print("README 는 읽기 전용입니다. 이 sample_config 을 config 파일로 확장하되, 그냥 이름만 바꾸고 여기에 있는 요소들을 바꿔서는 안 됩니다. "
          "만약 이 경고를 무시할 경우, 당신에게 나쁜 영향을 끼칠 것이란 것을 알려드립니다.\n봇 종료.", file=sys.stderr)
    quit(1)


class Config(object):
    TOKEN = ''  # 봇 토큰
    OWNERS = [123456789]  # 관리자의 아이디
    DEBUG_SERVER = []  # 채널 id
    BOT_NAME = ""  # 봇 이름
    BOT_TAG = "#"  # 태그
    BOT_ID = 123456789  # 봇 아이디
    ABOUT_BOT = ""  # 봇 정보
    COLOR_CODE = 0xc68e6e  # 색상코드

    # Music
    HOST = "localhost"
    PSW = ""  # 컴퓨터 비밀번호
    REGION = "ko"  # 리전
    PORT = 2333
    LAVALINK_AUTO_UPDATE = True
    LAVALINK_PLUGINS = {
        # "com.github.topi314.lavasrc:lavasrc-plugin": "https://api.github.com/repos/topi314/LavaSrc/releases",
        "dev.lavalink.youtube:youtube-plugin": "https://api.github.com/repos/lavalink-devs/youtube-source/releases"
    }

    # 봇 홍보용 사이트
    KOREANBOT_TOKEN = None
    TOPGG_TOKEN = None

    # SQL
    SQL_HOST = "localhost"
    SQL_USER = "root"
    SQL_PASSWORD = ""
    SQL_DB = "tkbot"


class Production(Config):
    LOGGER = False


class Development(Config):
    LOGGER = True
