import asyncio
import sqlite3
import datetime

from musicbot.utils.statistics import StatisticsDb


async def add_today_table():
    while True:
        # Set path
        path = StatisticsDb().db_path
        # Connect db
        conn = sqlite3.connect(path, isolation_level=None)
        c = conn.cursor()
        # Set table name
        table_name = datetime2str(datetime.datetime.today())
        # Create table
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT, video_id text, count int)")
        conn.close()

        # wait 1 day
        await asyncio.sleep(86400)


async def add_missing_table():
    # Set path
    path = StatisticsDb().db_path
    # Get table list
    table_list = get_table_list(path)
    # Set date
    today = datetime2str(datetime.datetime.today())
    # First date
    first_date = str2datetime(table_list[0][0])
    # Connect db
    conn = sqlite3.connect(path, isolation_level=None)
    c = conn.cursor()
    while datetime2str(first_date) != today:
        # Set table name
        table_name = datetime2str(first_date)
        # Create table
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT, video_id text, count int)")
        # Set date
        first_date += datetime.timedelta(days=1)
    conn.close()


def str2datetime(date: str) -> datetime.datetime:
    date_time_obj = datetime.datetime.strptime(date, 'date%Y%m%d')
    return date_time_obj


def datetime2str(date: datetime.datetime):
    str_date = date.strftime("date%Y%m%d")
    return str_date


def get_table_list(path) -> list[str]:
    """ 테이블 리스트 반환 """
    conn = sqlite3.connect(path, isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM sqlite_sequence ORDER BY name ASC")  # 오름차순으로 정렬
    table_list = c.fetchall()
    conn.close()

    return table_list


def duplicate_processing() -> None:  # 데이터베이스 읽기가 안됐을 때 중복 생성된 레코드 처리
    path = StatisticsDb().db_path
    table_list = get_table_list(path)

    conn = sqlite3.connect(path, isolation_level=None)
    c = conn.cursor()
    for table in table_list:
        c.execute(f"SELECT * FROM {table[0]}")
        data = c.fetchall()
        temp_data = {}
        for d in data:
            try:
                temp_data[d[1]] += 1
            except KeyError:
                temp_data[d[1]] = 1

        print(temp_data)

        c.execute(f"DELETE FROM {table[0]}")
        c.execute(f"UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = '{table[0]}'")
        c.execute(f"CREATE TABLE IF NOT EXISTS {table[0]} (id integer PRIMARY KEY AUTOINCREMENT, video_id text, count int)")
        for video_id, num in temp_data.items():
            c.execute(f"INSERT INTO {table[0]} (video_id, count) VALUES('{video_id}', {num})")

    conn.close()