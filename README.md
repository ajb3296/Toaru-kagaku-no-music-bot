# Toaru-kagaku-no-music-bot

<a href="https://discord.gg/etzmFDGFVg"><img src="https://img.shields.io/discord/803935936219578368?color=7289da&logo=discord&logoColor=white" alt="Discord server" /></a>
<a href="https://discord.com/oauth2/authorize?client_id=714140461840728144&permissions=3165184&scope=bot"><img src="https://api.koreanbots.dev/widget/bots/servers/714140461840728144.svg" alt="Server count" /></a>
<a href="https://www.codefactor.io/repository/github/ajb3296/toaru-kagaku-no-music-bot"><img src="https://www.codefactor.io/repository/github/ajb3296/toaru-kagaku-no-music-bot/badge" alt="CodeFactor" /></a>

[English README](https://github.com/ajb3296/Toaru-kagaku-no-music-bot/blob/main/README.en.md)

## Heroku Deploy

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/ajb3296/Toaru-kagaku-no-music-bot/tree/main)

## Note

[Lavalink Download](https://github.com/freyacodes/Lavalink/releases)<br>
[Lavalink Download(for arm or 32bit)](https://github.com/Cog-Creators/Lavalink-Jars/releases)

* 이 프로그램은 [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html) 을 따릅니다.

### 참고

* [lavalink.py](https://github.com/Devoxin/Lavalink.py)
* [EZPaginator](https://github.com/khk4912/EZPaginator)

## How to install

### Heroku 로 사용하는 방법

1. 위 Heroku Deploy 버튼을 누른다.
2. 기초 설정을 한다.
3. Deploy 한다.

### 컴퓨터로 사용하는 방법

1. `musicbot` 폴더 안에 `config.py` 파일을 만든다.
2. `config.py` 파일을 아래와 같이 작성한다.
```python
from musicbot.sample_config import Config

class Development(Config):
    TOKEN = '토큰'
    OWNERS = [관리자 디스코드 아이디]
    DebugServer = [디버그 서버 id]
    commandInt = "명령인자"
    BOT_NAME = "봇 이름"
    BOT_TAG = "#봇태그"
    BOT_ID = 봇아이디
    AboutBot = f"""봇 정보(about 명령어)에 넣을 말"""

    # Music
    psw = "컴퓨터 비밀번호"
```
`sample_config.py`를 **참고** 하여 만드시면 됩니다.<br>
3. `python -m musicbot` 명령어를 실행한다.
