"""
volume:
    guild_id: int
    volume: int

loop:
    guild_id: int
    loop: int
"""

import sqlite3

class Database():
    def __init__(self):
        self.path = "database.db"
        self.loop_table = "loop"

    def set_pid(self, pid: int):
        """ lavalink pid 저장 """
        con = sqlite3.connect(self.path, isolation_level=None)
        cur = con.cursor()
        
        # read pid from lavalink table
        cur.execute("SELECT * FROM lavalink")

        con.close()
    
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