# For windows

import os
import re
from unicodedata import normalize

anilist_path = "musicbot/anilist"

files = []
for file in os.listdir(anilist_path):
    #if file.endswith(".txt"):
    files.append(file)

for file in files:
    file_oldname = os.path.join(anilist_path, file)
    # remove \ / : * ? " < > |
    file_newname_newfile = os.path.join(anilist_path, re.sub("\\|\/|\:|\*|\?|\"|\<|\>|\|","", file))

    os.rename(file_oldname, file_newname_newfile)

    before_filename = os.path.join(anilist_path, file)
    after_filename = normalize('NFC', before_filename)
    os.rename(before_filename, after_filename)

print("Finish")