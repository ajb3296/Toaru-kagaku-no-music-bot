<div align="center">
    <img align="left" class="fit-picture" src="./image/tk-musicbot-head-circle.png" alt="Toaru-kagaku-no-musicbot" width="200px" height="200px">
    <div align="left">
        <h1>Toaru Kagaku no musicbot</h1>
        <a>사용하기 쉽고 편한, 여러 편의기능이 있는 디스코드 음악봇</a><br><br>
        <a href="https://github.com/ajb3296/Toaru-kagaku-no-music-bot/blob/main/README.en.md"><img src="https://img.shields.io/badge/README-EN-blue" alt="English README"></a><br>
        <a href="https://discord.gg/etzmFDGFVg"><img src="https://img.shields.io/discord/803935936219578368?color=7289da&logo=discord&logoColor=white" alt="Discord server" /></a>
        <a href="https://discord.com/oauth2/authorize?client_id=714140461840728144&permissions=3165184&scope=bot"><img src="https://koreanbots.dev/api/widget/bots/servers/714140461840728144.svg" alt="Server count" /></a>
        <a href="https://www.codefactor.io/repository/github/ajb3296/toaru-kagaku-no-music-bot"><img src="https://www.codefactor.io/repository/github/ajb3296/toaru-kagaku-no-music-bot/badge" alt="CodeFactor" /></a>
        <a href="https://www.codacy.com/gh/ajb3296/Toaru-kagaku-no-music-bot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ajb3296/Toaru-kagaku-no-music-bot&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/a077da0e48aa4adbad939e0e43042e60" alt="Codacy"/></a>
    </div>
</div>
<br><br>
<a href="https://www.instagram.com/jsl__054"><img src="https://img.shields.io/badge/Illustrator_Instagram-E4405F?style=flat&logo=Instagram&logoColor=white" alt="Illustrator_Instagram"></a>

## Features

* Lavalink 자동 업데이트
* 이퀄라이저 지원

## Note

[Lavalink Download](https://github.com/freyacodes/Lavalink/releases)<br>
[Lavalink Download(for arm or 32bit)](https://github.com/Cog-Creators/Lavalink-Jars/releases)

* [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.html) 라이선스를 따릅니다.

### 참고

* [lavalink.py](https://github.com/Devoxin/Lavalink.py)
* [EZPaginator](https://github.com/khk4912/EZPaginator)
* [soundcloud-lib](https://github.com/3jackdaws/soundcloud-lib)

## 설치법

1. `python -m musicbot` 명령어를 실행한다.
2. 프로그램의 안내에 따라 진행한다

## Dashboard

[Github](https://github.com/ajb3296/Toaru-kagaku-no-music-bot-dashboard) - 개발 중

## 알려진 버그

* Equalizer 부동소수점 연산 버그로 그래프가 똑바로 표기되지 않을 수 있음.

## Docker
```bash
git clone https://github.com/ajb3296/Toaru-kagaku-no-music-bot.git
```
명령어를 통해 레포지토리를 클론하고 해당 디렉토리로 이동합니다.
<br /><br />
이후 .env 파일을 아래와 같이 작성합니다.

### .env 파일 예시
```bash
ENV="True"

TOKEN=""  # 봇 토큰
OWNERS=""  # 관리자의 아이디 (쉼표로 구분)
DEBUG_SERVER=""  # 디버그 서버 아이디 (쉼표로 구분)
BOT_NAME=""  # 봇 이름
BOT_TAG="#"  # 태그
BOT_ID="123456789"  # 봇 아이디
ABOUT_BOT=""  # 봇 정보
COLOR_CODE="0xc68e6e"  # 색상코드
```

### 사용 가능한 변수

| 변수 | 설명 | 예시 |
|---|---|---|
| ENV | 환경 설정, Docker 사용 시 True 필수 | True |
| TOKEN | 봇 토큰 | token 값 |
| OWNERS | 관리자의 아이디 (쉼표로 구분) | 123456789012345678,987654321098765432 |
| DEBUG_SERVER | 디버그 서버 아이디 (쉼표로 구분) | 123456789012345678,987654321098765432 |
| BOT_NAME | 봇 이름 | MyMusicBot |
| BOT_TAG | 디스코드 태그 | #1234 |
| BOT_ID | 봇 아이디 | 123456789012345678 |
| ABOUT_BOT | 봇 정보 | 이 봇은 음악을 재생합니다. |
| COLOR_CODE | 색상 코드 | 0xc68e6e |
| START_WITH_LAVALINK | Lavalink 를 함께 실행할지 여부 | True |
| HOST | Lavalink 호스트 주소 | localhost |
| PSW | Lavalink 작동에 필요한 컴퓨터 비밀번호 | mypassword |
| REGION | 리전 (US, EU 등) | US |
| PORT | Lavalink 포트 | 2333 |
| LAVALINK_AUTO_UPDATE | Lavalink.jar 자동 업데이트 여부 | True |
| LAVALINK_PLUGINS | Lavalink 플러그인 (쉼표로 구분) | plugin1,plugin2 |
| KOREANBOT_TOKEN | KoreanBot 토큰 | mykoreanbottoken |
| TOPGG_TOKEN | Top.gg 토큰 | mytopggtoken |
| SQL_HOST | 외부 MySQL 호스트 주소 | localhost |
| SQL_USER | 외부 MySQL 사용자 이름 | root |
| SQL_PASSWORD | 외부 MySQL 비밀번호 | mypassword |
| SQL_DB | 외부 MySQL 데이터베이스 이름 | tkbot |
| USING_IPV6_TUNNELING | IPV6 터널링 사용 여부 | False |
| IP_BLOCKS | 쉼표로 구분된 IP 블록 (예: "2001:db8::/32,2001:db9::/32") | 2001:db8::/32,2001:db9::/32 |
| EXCLUDE_IPS | 제외할 IP (쉼표로 구분) | 2001:db8::1,2001:db8::2 |
| STRATEGY | IPV6 전략 (RotateOnBan, LoadBalance 등) | RotateOnBan |

### Docker 실행 명령어
```bash
docker compose up -d
```