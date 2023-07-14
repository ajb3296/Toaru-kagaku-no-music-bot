"""
loop:
    guild_id: int
    loop: int

shuffle:
    guild_id: int
    shuffle: int
"""

import pymysql
from musicbot import SQL_HOST, SQL_USER, SQL_PASSWORD, SQL_DB


class Database:
    def __init__(self):
        self.loop_table = "loop_setting"
        self.shuffle_table = "shuffle"

    def set_loop(self, guild_id: int, loop: int) -> None:
        """ 길드 아이디로 루프 저장 """
        con = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DB, charset='utf8')
        cur = con.cursor()

        guild = str(guild_id)

        # read loop
        cur.execute(f"SELECT * FROM {self.loop_table} WHERE guild_id=%s", (guild))
        db_loop = cur.fetchone()
        if db_loop is None:
            # add loop
            cur.execute(f"INSERT INTO {self.loop_table} VALUES(%s, %s)", (guild, loop))
        else:
            # modify loop
            cur.execute(f"UPDATE {self.loop_table} SET loop_set=%s WHERE guild_id=%s", (loop, guild))

        con.commit()
        con.close()

    def get_loop(self, guild_id: int) -> int | None:
        """ 모든 루프설정 가져오기 """
        con = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DB, charset='utf8')
        cur = con.cursor()

        # read loop
        cur.execute(f"SELECT * FROM {self.loop_table} WHERE guild_id=%s", (str(guild_id)))
        loop = cur.fetchone()
        con.close()

        if loop is not None:
            loop = loop[1]

        return loop

    def set_shuffle(self, guild_id: int, shuffle: bool) -> None:
        """ 길드 아이디로 셔플 저장 """
        con = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DB, charset='utf8')
        cur = con.cursor()

        guild = str(guild_id)

        # read shuffle
        cur.execute(f"SELECT * FROM {self.shuffle_table} WHERE guild_id=%s", (guild))
        db_shuffle = cur.fetchone()
        if db_shuffle is None:
            # add shuffle
            cur.execute(f"INSERT INTO {self.shuffle_table} VALUES(%s, %s)", (guild, shuffle))
        else:
            # modify shuffle
            cur.execute(f"UPDATE {self.shuffle_table} SET shuffle=%s WHERE guild_id=%s", (shuffle, guild))

        con.commit()
        con.close()

    def get_shuffle(self, guild_id: int) -> bool | None:
        """ 모든 셔플설정 가져오기 """
        con = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DB, charset='utf8')
        cur = con.cursor()

        # read shuffle
        cur.execute(f"SELECT * FROM {self.shuffle_table} WHERE guild_id=%s", (str(guild_id)))
        shuffle = cur.fetchone()
        con.close()

        if shuffle is not None:
            shuffle = shuffle[1]

        return shuffle
