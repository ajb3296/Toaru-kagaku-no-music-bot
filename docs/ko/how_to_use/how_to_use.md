# 사용법

## Heroku 로 사용하는 방법

1. 위 Heroku Deploy 버튼을 누른다.
2. 기초 설정을 한다.
3. Deploy 한다.

## 컴퓨터로 사용하는 방법

1. `musicbot` 폴더 안에 `config.py` 파일을 만든다.
2. `config.py` 파일을 아래와 같이 작성한다.
```python
from musicbot.sample_config import Config

class Development(Config):
    TOKEN = '토큰'
    OWNERS = [관리자 디스코드 아이디]
    DebugServer = [디버그 서버 id]
    BOT_NAME = "봇 이름"
    BOT_TAG = "#봇태그"
    BOT_ID = 봇아이디
    AboutBot = f"""봇 정보(about 명령어)에 넣을 말"""

    # Music
    psw = "컴퓨터 비밀번호"
```
`sample_config.py`를 **참고** 하여 만드시면 됩니다.<br>
3. `python -m musicbot` 명령어를 실행한다.

# 봇의 사용법

버전별로 사용법이 다르므로 최신버전 기준 discord에서 봇에게 SlashCommand로 `/help`를 입력 후 알고 싶은 항목을 선택하시면 사용법을 보내줍니다.