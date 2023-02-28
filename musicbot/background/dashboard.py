import os
import time
import requests

from musicbot import LOGGER

def dashboard_check():
    while True:
        post = None
        try:
            post = requests.post("http://127.0.0.1:8000/path/", json={"path": os.getcwd()})
        except requests.exceptions.ConnectionError:
            pass
        # 접속 성공했을 경우
        if post is not None and post.status_code == 200:
            LOGGER.info("Dashboard connected")
            time.sleep(3600)
        else:
            LOGGER.error("Dashboard connection failed")
            time.sleep(30)