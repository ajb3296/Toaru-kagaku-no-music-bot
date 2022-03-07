"""

Table name example : date20220101

ID, video_id, count

"""

import os
import sqlite3
from datetime import datetime

statistics_db_path = "statistics.db"

class Statistics:
    def up(video_id):
        # Get play count from db
        statisticsdb = Statistics_Db
        temp = statisticsdb.get(video_id)
        # Set count
        if temp is None:
            num = 1
        else:
            num = temp[2] + 1
        statisticsdb.write(video_id, num)

    # 이게 왜 필요했더라...언젠간 쓰겠지
    def down(video_id):
        # if the statistics_db_path file exists
        if os.path.exists(statistics_db_path):
            # Get play count from db
            statisticsdb = Statistics_Db
            temp = statisticsdb.get(video_id)
            # Set count
            if temp is None:
                num = 1
            else:
                num = temp[2] - 1
            statisticsdb.write(video_id, num)

class Statistics_Db:
    def get(video_id):
        conn = sqlite3.connect(statistics_db_path, isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM date{datetime.today().strftime('%Y%m%d')} WHERE video_id=:Id", {"Id": video_id})
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp
    
    def get_all(table_name):
        conn = sqlite3.connect(statistics_db_path, isolation_level=None)
        c = conn.cursor()
        # 내림차순으로 정렬
        try:
            c.execute(f"SELECT * FROM {table_name} ORDER BY count DESC")
        except sqlite3.OperationalError:
            return None
        temp = c.fetchall()
        conn.close()
        return temp

    def write(video_id, edit_count = 1):
        # Create table if it doesn't exist
        conn = sqlite3.connect(statistics_db_path, isolation_level=None)
        c = conn.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS date{datetime.today().strftime('%Y%m%d')} (id integer PRIMARY KEY AUTOINCREMENT, video_id text, count int)")

        if edit_count == 1:
            # add music count
            c.execute(f"INSERT INTO date{datetime.today().strftime('%Y%m%d')} (video_id, count) VALUES('{video_id}', {edit_count})")
        else:
            # modify music count
            c.execute(f"UPDATE date{datetime.today().strftime('%Y%m%d')} SET count=:count WHERE video_id=:video_id", {"count": edit_count, 'video_id': video_id})
        conn.close()

if __name__ == "__main__":
    # For test
    statistics = Statistics
    statistics.up("Youtube_video_id")