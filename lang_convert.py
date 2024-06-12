# 미완성

import re
import os
import json

regex = re.compile(r'get_lan\(ctx\.author\.id, "([a-z_]+)"\)')

def get_lang_file(path: str):
    file = open(path, "r")
    data = json.load(file)
    file.close()

    return data

if __name__ == "__main__":
    # 새 언어파일 생성
    ko = get_lang_file("musicbot/languages/ko.json")
    en = get_lang_file("musicbot/languages/en.json")

    new_ko = {}
    new_en = {}

    for i in ko:
        new_ko[ko[i]] = ko[i]
        new_en[ko[i]] = en[i]

    # 파일 목록
    file_list = os.listdir("musicbot/cogs")
    file_list = [file for file in file_list if file.endswith(".py")]

    for file in file_list:
        file_path = f"musicbot/cogs/{file}"
        file = open(file_path, "r")
        lines = file.readlines()
        file.close()

        for i, line in enumerate(lines):
            regex_result = regex.search(line)


        with open(file_path, "w") as f:
            f.writelines(lines)