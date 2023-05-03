import os
import re
import time
import json
import requests
import datetime
import subprocess
from urllib import request

from musicbot import LOGGER


def get_lavalink_ver() -> tuple[str | None, str]:
    """ lavalink 최신버전 가져오기 """
    # 최신 라바링크 버전
    latest_lavalink_tag = json.loads(requests.get("https://api.github.com/repos/freyacodes/Lavalink/releases").text)[0][
        'tag_name']

    # 현재 라바링크 버전
    now_lavalink_ver = None
    if os.path.exists("Lavalink.jar"):
        lavalink_ver = subprocess.check_output(
            ['java', '-jar', 'Lavalink.jar', '--version'],
            stderr=subprocess.STDOUT,
            encoding='utf-8'
        )
        now_lavalink_ver = re.search(r"Version:\s+(\d+\.\d+\.\d+)", lavalink_ver)
        if now_lavalink_ver is not None:
            now_lavalink_ver = now_lavalink_ver.group(1)

    return now_lavalink_ver, latest_lavalink_tag


def download_lavalink() -> None:
    """ lavalink 최신버전 체크 후 다운로드 """
    # 최신 라바링크 버전과 다를 경우
    now_lavalink_ver, latest_lavalink_tag = get_lavalink_ver()
    if now_lavalink_ver != latest_lavalink_tag:
        LOGGER.info("Latest Lavalink downloading...")
        LOGGER.info(f"v{now_lavalink_ver} -> v{latest_lavalink_tag}")
        lavalink_download_link = f"https://github.com/freyacodes/Lavalink/releases/download/{latest_lavalink_tag}/Lavalink.jar"

        request.urlretrieve(lavalink_download_link, "Lavalink.jar")


def start_lavalink() -> None:
    """ lavalink 시작, multiprocessing으로 실행해야 함 """
    while True:
        # Start lavalink
        sp = subprocess.Popen(["java", "-jar", "Lavalink.jar"])
        LOGGER.info(f"Lavalink PID: {sp.pid}")
        while True:
            # 1시간 대기
            time.sleep(3600)
            # 만약 새벽 4시라면
            if datetime.datetime.now().hour == 4:
                # 만약 새 버전이 나왔다면
                now_lavalink_ver, latest_lavalink_tag = get_lavalink_ver()
                if now_lavalink_ver != latest_lavalink_tag:
                    # Lavalink Download
                    download_lavalink()
                    # Shutdown lavalink
                    sp.terminate()
                    LOGGER.info("Lavalink shutdown")
                    break
