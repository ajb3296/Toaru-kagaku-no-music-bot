"""

Table name example : date20220101

ID, video_id, count

"""

import sqlite3
from datetime import datetime, timedelta

class Statistics:
    def __init__(self):
        self.statisticsdb = StatisticsDb()

    def up(self, video_id: str) -> None:
        """ 비디오 재생 횟수를 1 증가시킵니다 """
        # Set table name
        table_name = f"date{datetime.today().strftime('%Y%m%d')}"
        # Get play count from db
        temp = self.statisticsdb.get(table_name, video_id)
        # Set count
        if temp is None:
            num = 1
        else:
            num = temp[2] + 1
        self.statisticsdb.write(table_name, video_id, num)
    
    def get_week(self) -> dict[str, int]:
        """ 이번주의 통계를 가져옵니다 """
        week_data = {}
        for day in range(7): # 0 ~ 6
            # 타깃 날짜 설정
            target_date = datetime.today() - timedelta(days=day)
            table_name = f"date{target_date.strftime('%Y%m%d')}"

            # 해당 날짜의 데이터 가져오기
            videos_data = self.statisticsdb.get_all(table_name)
            if videos_data is not None:
                for data in videos_data:
                    _, video_id, count = data
                    week_data[video_id] = count

        return week_data

class StatisticsDb:
    def __init__(self):
        self.db_path = "statistics.db"

    def get(self, table_name: str, video_id: str) -> tuple[int, str, int] | None:
        """ 비디오 아이디로 데이터를 가져옴 """
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

    def get_all(self, table_name: str) -> list[tuple[int, str, int]] | None:
        """ 테이블의 모든 데이터를 가져옴 """
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

    def write(self, table_name: str, video_id: str, edit_count: int = 1) -> None:
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
    statistics = Statistics()
    statistics.up("Youtube_video_id")