import os
import json
import pymysql

from musicbot import SQL_HOST, SQL_USER, SQL_PASSWORD, SQL_DB


def get_lan(user_id, text: str):
    """ user_id 가 선택한 언어를 반환 """
    default_language = "en"

    # if the userdata file exists
    con = pymysql.connect(host=SQL_HOST, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DB, charset='utf8')
    cur = con.cursor()
    cur.execute("SELECT * FROM language WHERE id=%s", (str(user_id)))
    temp = cur.fetchone()
    if temp is None:
        language = default_language
    else:
        language = temp[1]
        if not os.path.exists(f"musicbot/languages/{language}.json"):
            language = default_language
    con.close()
    # read language file
    with open(f"musicbot/languages/{language}.json", encoding="utf-8") as f:
        language_data = json.load(f)
    return language_data[text]