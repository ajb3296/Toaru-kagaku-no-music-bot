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
    # 기존 언어파일 가져오기
    ko = get_lang_file("musicbot/languages/ko.json")
    en = get_lang_file("musicbot/languages/en.json")

    # 새 언어파일 생성
    new_ko = {}
    new_en = {}

    for i in ko:
        new_ko[ko[i]] = ko[i]
        new_en[ko[i]] = en[i]

    # 파일 목록
    file_list = os.listdir("musicbot/utils")
    file_list = [file for file in file_list if file.endswith(".py")]

    for file in file_list:
        file_path = f"musicbot/utils/{file}"

        # 모듈 읽기
        file = open(file_path, "r")
        lines = file.readlines()
        file.close()

        file = open(file_path, "w")
        for i, line in enumerate(lines):
            regex_result = regex.search(line)
            if regex_result:
                file.write(regex.sub('get_lan(ctx.author.id, "' + ko[regex_result.groups()[0]] + '")', line))
            else:
                file.write(line)
        file.close()


    # 언어파일 저장
    file = open("musicbot/languages/new_ko.json", "w")
    json.dump(new_ko, file, indent=4, ensure_ascii=False)
    file.close()

    file = open("musicbot/languages/new_en.json", "w")
    json.dump(new_en, file, indent=4, ensure_ascii=False)
    file.close()
