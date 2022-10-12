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
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (video_id TEXT, count INTEGER)")
        conn.close()

        # wait 1 day
        await asyncio.sleep(86400)

async def add_missing_table():
    # Set path
    path = StatisticsDb().db_path
    # Get table list
    table_list = get_table_list()
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
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (video_id TEXT, count INTEGER)")
        # Set date
        first_date += datetime.timedelta(days=1)
    conn.close()

def str2datetime(date):
    date_time_obj = datetime.datetime.strptime(date, 'date%Y%m%d')
    return date_time_obj

def datetime2str(date):
    str_date = date.strftime("date%Y%m%d")
    return str_date

def get_table_list():
    path = "/Users/anjaebeom/Desktop/statistics.db"
    conn = sqlite3.connect(path, isolation_level=None)
    c = conn.cursor()
    c.execute("SELECT * FROM sqlite_sequence ORDER BY name ASC") # 오름차순으로 정렬
    table_list = c.fetchall()
    conn.close()

    return table_list