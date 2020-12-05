# Toaru-kagaku-no-music-bot
## 현재 개발중이므로 헤로쿠에서 작동하지 않습니다!
일반 컴퓨터에서는 잘 굴러갑니다 :)
## Heroku Deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/NewPremium/Toaru-kagaku-no-music-bot/tree/main)

## Note

[Lavalink Download](https://github.com/Cog-Creators/Lavalink-Jars/releases)

* 이 프로그램은 [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html) 을 따릅니다.
* `멜론재생` 명령어는 이 레포지스터리 Star 100개 이상 혹은 [어떤 과학의 음악봇](https://discord.com/oauth2/authorize?client_id=714140461840728144&permissions=3165184&scope=bot) 이 공식봇이 된다면 공개하겠습니다. [어떤 과학의 음악봇](https://discord.com/oauth2/authorize?client_id=714140461840728144&permissions=3165184&scope=bot) 에서 `멜론재생` 명령어를 체험해 보실 수 있습니다.

## How to install

### Heroku 로 사용하는 방법

1. 위 Heroku Deploy 버튼을 누른다.
2. 기초 설정을 한다.
3. Deploy 한다.

### 컴퓨터로 사용하는 방법

1. `musicbot` 폴더 안에 `config.py` 파일을 만든다.
2. `config.py` 파일을 아래와 같이 작성한다.
```
from musicbot.sample_config import Config

class Development(Config):
    TOKEN = '봇 토큰'
    OWNERS = [관리자 디스코드 아이디]
    commandInt = "명령인자"
    BOT_NAME = "봇 이름"
    BOT_TAG = "#봇태그"
    BOT_VER = "버전"
    BOT_ID = 봇아이디
    AboutBot = f"""봇 정보(about 명령어)에 넣을 말"""

    # Music
    psw = "컴퓨터 비밀번호"
    name = "컴퓨터 이름"
```
`sample_config.py`를 **참고** 하여 만드시면 됩니다.<br>
3. `python -m musicbot` 명령어를 실행한다.
