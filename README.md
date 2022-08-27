# Toaru-kagaku-no-music-bot

<a href="https://discord.gg/etzmFDGFVg"><img src="https://img.shields.io/discord/803935936219578368?color=7289da&logo=discord&logoColor=white" alt="Discord server" /></a>
<a href="https://discord.com/oauth2/authorize?client_id=714140461840728144&permissions=3165184&scope=bot"><img src="https://koreanbots.dev/api/widget/bots/servers/714140461840728144.svg" alt="Server count" /></a>
<a href="https://www.codefactor.io/repository/github/ajb3296/toaru-kagaku-no-music-bot"><img src="https://www.codefactor.io/repository/github/ajb3296/toaru-kagaku-no-music-bot/badge" alt="CodeFactor" /></a>
<a href="https://www.codacy.com/gh/ajb3296/Toaru-kagaku-no-music-bot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ajb3296/Toaru-kagaku-no-music-bot&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/a077da0e48aa4adbad939e0e43042e60" alt="Codacy"/></a>

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

1. `python -m musicbot` 명령어를 실행한다.
2. 프로그램의 안내에 따라 진행한다

### Troubleshoot

차트 사이트 파싱중 SSL 인증서 관련 문제가 발생했을 경우 :<br>

`/etc/ssl/openssl.cnf` 파일을 연 후 `CipherString`을 `DEFAULT@SECLEVEL=2`에서 `DEFAULT@SECLEVEL=1`로 변경 후 시스템을 재부팅 합니다.<br>

도움 주신분 : [KeonWoo PARK](https://github.com/parkkw472)