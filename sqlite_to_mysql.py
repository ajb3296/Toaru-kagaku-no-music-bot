import re
import sqlite3
import pymysql
from datetime import datetime

SQL_HOST = "localhost"
SQL_USER = "root"
SQL_PASSWORD = ""
SQL_DB = "tkbot"


# 통계 데이터
sqlite_con = sqlite3.connect("statistics.db")
sqlite_cur = sqlite_con.cursor()

# 테이블 리스트 가져오기
sqlite_cur.execute("SELECT * FROM sqlite_sequence ORDER BY name ASC")
table_list = sqlite_cur.fetchall()

statistics = []

for table in table_list:
    table_name = table[0]
    sqlite_cur.execute(f"SELECT * FROM {table_name}")

    date = datetime.strptime(table_name, 'date%Y%m%d')
    date = date.strftime("%Y-%m-%d")

    data = sqlite_cur.fetchall()
    for row in data:
        video_id = row[1]
        count = row[2]
        statistics.append((date, video_id, count))

sqlite_con.close()


sqlite_con = sqlite3.connect("userdata.db")
sqlite_cur = sqlite_con.cursor()

sqlite_cur.execute("SELECT * FROM userdata")
userdata = sqlite_cur.fetchall()

sqlite_con.close()




sqlite_con = sqlite3.connect("database.db")
sqlite_cur = sqlite_con.cursor()

sqlite_cur.execute("SELECT * FROM loop")
loop = sqlite_cur.fetchall()
sqlite_cur.execute("SELECT * FROM shuffle")
shuffle = sqlite_cur.fetchall()

sqlite_con.close()



con = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db='tkbot', charset='utf8')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS statistics (date date, video_id text, count int)")
cur.execute("CREATE TABLE IF NOT EXISTS language (id text, language text)")
cur.execute("CREATE TABLE IF NOT EXISTS loop_setting (guild_id text, loop_set int)")
cur.execute("CREATE TABLE IF NOT EXISTS shuffle (guild_id text, shuffle bool)")

url_rx = re.compile(r'(.+)?https?://(?:www\.)?.+')
for i in statistics:
    if not url_rx.match(i[1]):
        cur.execute("INSERT INTO statistics (date, video_id, count) VALUES (%s, %s, %s)", (i[0], i[1], i[2]))

for i in userdata:
    cur.execute("INSERT INTO language (id, language) VALUES (%s, %s)", (str(i[0]), i[1]))

for i in loop:
    cur.execute("INSERT INTO loop_setting (guild_id, loop_set) VALUES (%s, %s)", (str(i[0]), i[1]))

for i in shuffle:
    cur.execute("INSERT INTO shuffle (guild_id, shuffle) VALUES (%s, %s)", (str(i[0]), i[1]))

con.commit()
con.close()