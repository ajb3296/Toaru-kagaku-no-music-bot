if not __name__.endswith("sample_config"):
    import sys
    print("README 는 읽기 전용입니다. 이 sample_config 을 config 파일로 확장하되, 그냥 이름만 바꾸고 여기에 있는 요소들을 바꿔서는 안 됩니다. "
          "만약 이 경고를 무시할 경우, 당신에게 나쁜 영향을 끼칠 것이란 것을 알려드립니다.\n봇 종료.", file=sys.stderr)
    quit(1)

class Config(object):
    TOKEN = '' # 봇 토큰
    EXTENSIONS = ['owners',
                'help',
                'other',
                'ping',
                'about',
                'music']

    OWNERS = [123456789] # 관리자의 아이디
    commandInt = "" # 명령인자
    BOT_NAME = "" # 봇 이름
    BOT_TAG = "#" # 태그
    BOT_VER = "" # 버전
    BOT_ID = 123456789      # 봇 아이디
    AboutBot = "" # 봇 정보

    # Music
    host = "localhost"
    psw = "" # 컴퓨터 비밀번호
    region = "eu" # 리전
    port = 2333

    color_code = 0xc68e6e # 색상코드

class Production(Config):
    LOGGER = False

class Development(Config):
    LOGGER = True
