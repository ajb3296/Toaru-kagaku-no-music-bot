"""
loop:
    guild_id: int
    loop: int

shuffle:
    guild_id: int
    shuffle: int
"""

import sqlite3


class Database:
    def __init__(self):
        self.path = "database.db"
        self.loop_table = "loop"
        self.shuffle_table = "shuffle"

    def set_loop(self, guild: int, loop: int) -> None:
        """ 길드 아이디로 루프 저장 """
        con = sqlite3.connect(self.path, isolation_level=None)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS userdata (guild_id int PRIMARY KEY, loop int)")

        # read loop
        cur.execute(f"SELECT * FROM {self.loop_table} WHERE guild_id=:guild_id", {"guild_id": guild})
        db_loop = cur.fetchone()
        if db_loop is None:
            # add loop
            cur.execute(f"INSERT INTO {self.loop_table} VALUES(?, ?)", (guild, loop))
        else:
            # modify loop
            cur.execute(f"UPDATE {self.loop_table} SET loop=:loop WHERE guild_id=:guild_id", {"loop": loop, 'guild_id': guild})

        con.close()

    def get_loop(self, guild_id: int) -> int | None:
        """ 모든 루프설정 가져오기 """
        con = sqlite3.connect(self.path, isolation_level=None)
        cur = con.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.loop_table} (guild_id int PRIMARY KEY, loop int)")

        # read loop
        cur.execute(f"SELECT * FROM {self.loop_table} WHERE guild_id=:guild_id", {"guild_id": guild_id})
        loop = cur.fetchone()
        con.close()

        if loop is not None:
            loop = loop[1]

        return loop

    def set_shuffle(self, guild: int, shuffle: bool) -> None:
        """ 길드 아이디로 셔플 저장 """
        con = sqlite3.connect(self.path, isolation_level=None)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS userdata (guild_id int PRIMARY KEY, shuffle bool)")

        # read shuffle
        cur.execute(f"SELECT * FROM {self.shuffle_table} WHERE guild_id=:guild_id", {"guild_id": guild})
        db_shuffle = cur.fetchone()
        if db_shuffle is None:
            # add shuffle
            cur.execute(f"INSERT INTO {self.shuffle_table} VALUES(?, ?)", (guild, shuffle))
        else:
            # modify shuffle
            cur.execute(f"UPDATE {self.shuffle_table} SET shuffle=:shuffle WHERE guild_id=:guild_id", {"shuffle": shuffle, 'guild_id': guild})

        con.close()

    def get_shuffle(self, guild_id: int) -> bool | None:
        """ 모든 셔플설정 가져오기 """
        con = sqlite3.connect(self.path, isolation_level=None)
        cur = con.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS {self.shuffle_table} (guild_id int PRIMARY KEY, shuffle bool)")

        # read shuffle
        cur.execute(f"SELECT * FROM {self.shuffle_table} WHERE guild_id=:guild_id", {"guild_id": guild_id})
        shuffle = cur.fetchone()
        con.close()

        if shuffle is not None:
            shuffle = shuffle[1]

        return shuffle
