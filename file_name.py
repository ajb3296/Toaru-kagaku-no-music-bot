# For windows

import os
import re

anilist_path = "musicbot/anilist"

files = []
for file in os.listdir(anilist_path):
    if file.endswith(".txt"):
        files.append(file)

for file in files:
    file_oldname = os.path.join(anilist_path, file)
    file_newname_newfile = os.path.join(anilist_path, re.sub("\\|\/|\:|\*|\?|\"|\<|\>|\|","", file))

    os.rename(file_oldname, file_newname_newfile)

print("Finish")