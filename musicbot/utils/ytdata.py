"""
cache:
    video_id: str
    title: str
    author: str
"""

import json
import sqlite3
import requests


class YTData:
    def __init__(self):
        self.cache_db = "cache.db"
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}

    def get(self, video_id: str) -> tuple[str, str, str]:
        """ 비디오 정보 가져오기 """
        # DB에 정보가 존재한다면 리턴
        db_data = self.db_get(video_id)
        if db_data is not None:
            return db_data
        # DB에 정보가 존재하지 않는다면 웹에서 가져오기
        video_data = requests.get(
            f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json",
            headers=self.header).text
        try:
            video_data = json.loads(video_data)
        except json.decoder.JSONDecodeError:
            return video_id, "Null", "Null"

        # DB에 정보 저장
        self.db_set(video_id, video_data["title"], video_data["author_name"])
        return video_id, video_data["title"], video_data["author_name"]

    def db_set(self, video_id: str, video_title: str, video_author: str) -> None:
        """ DB에 비디오 정보 저장 """
        con = sqlite3.connect(self.cache_db, isolation_level=None)
        cur = con.cursor()
        # if table not exists, create table
        cur.execute("CREATE TABLE IF NOT EXISTS cache (video_id text PRIMARY KEY, title text, author text)")
        # check video_id
        cur.execute(f"SELECT * FROM cache WHERE video_id=:video_id", {"video_id": video_id})
        db_video = cur.fetchone()
        if db_video is None:
            # add video
            cur.execute(f"INSERT INTO cache VALUES(?, ?, ?)", (video_id, video_title, video_author))
        else:
            # modify video
            cur.execute(f"UPDATE cache SET title=:title WHERE video_id=:video_id",
                        {"title": video_title, 'video_id': video_id})
            cur.execute(f"UPDATE cache SET title=:title WHERE author=:author",
                        {"title": video_title, 'author': video_author})
        con.close()

    def db_get(self, video_id: str) -> None | tuple[str, str, str]:
        """ DB에서 비디오 정보 가져오기 """
        con = sqlite3.connect(self.cache_db, isolation_level=None)
        cur = con.cursor()
        # if table not exists, create table
        cur.execute("CREATE TABLE IF NOT EXISTS cache (video_id text PRIMARY KEY, title text, author text)")
        cur.execute(f"SELECT * FROM cache WHERE video_id=:video_id", {"video_id": video_id})
        temp = cur.fetchone()
        con.close()
        return temp
