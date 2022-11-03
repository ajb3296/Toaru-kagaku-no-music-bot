"""

Table name example : date20220101

ID, video_id, count

"""

import sqlite3
from datetime import datetime

class Statistics:
    def up(video_id):
        # Set table name
        table_name = f"date{datetime.today().strftime('%Y%m%d')}"
        # Get play count from db
        statisticsdb = StatisticsDb()
        temp = statisticsdb.get(table_name, video_id)
        # Set count
        if temp is None:
            num = 1
        else:
            num = temp[2] + 1
        statisticsdb.write(table_name, video_id, num)

    # 이게 왜 필요했더라...언젠간 쓰겠지
    def down(video_id):
        # Set table name
        table_name = f"date{datetime.today().strftime('%Y%m%d')}"
        # Get play count from db
        statisticsdb = StatisticsDb()
        temp = statisticsdb.get(table_name, video_id)
        # Set count
        num = 1
        if temp is not None:
            num = temp[2] - 1
        statisticsdb.write(table_name, video_id, num)

class StatisticsDb:
    def __init__(self):
        self.db_path = "statistics.db"

    def get(self, table_name, video_id):
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM {table_name} WHERE video_id=:video_id", {"video_id": video_id})
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp

    def get_all(self, table_name):
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        # 내림차순으로 정렬
        try:
            c.execute(f"SELECT * FROM {table_name} ORDER BY count DESC")
        except sqlite3.OperationalError:
            return None
        temp = c.fetchall()
        conn.close()
        return temp

    def write(self, table_name, video_id, edit_count = 1):
        # Create table if it doesn't exist
        conn = sqlite3.connect(self.db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT, video_id text, count int)")

        if edit_count == 1:
            # add music count
            c.execute(f"INSERT INTO {table_name} (video_id, count) VALUES('{video_id}', {edit_count})")
        else:
            # modify music count
            c.execute(f"UPDATE {table_name} SET count=:count WHERE video_id=:video_id", {"count": edit_count, 'video_id': video_id})
        conn.close()


if __name__ == "__main__":
    # For test
    statistics = Statistics
    statistics.up("Youtube_video_id")