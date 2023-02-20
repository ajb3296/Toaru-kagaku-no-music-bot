import os
import json
import sqlite3

def get_lan(user_id, text: str):
    """ user_id 가 선택한 언어를 반환 """
    default_language = "en"
    userdata_db_path = "userdata.db"

    # if the userdata file exists
    if os.path.exists(userdata_db_path):
        con = sqlite3.connect(userdata_db_path, isolation_level=None)
        cur = con.cursor()
        cur.execute("SELECT * FROM userdata WHERE id=:Id", {"Id": user_id})
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

    else:
        with open(f"musicbot/languages/{default_language}.json", encoding="utf-8") as f:
            language_data = json.load(f)
        return language_data[text]