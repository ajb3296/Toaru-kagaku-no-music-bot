import re


def make_config() -> None:
    """ config.py 생성 """
    token = input("Enter your bot token : ")
    owners = input("Enter owners id, If there are multiple owners, separate them with a comma : ")
    owners = set(int(x) for x in owners.split(','))
    owners_result = ""
    for i in owners:
        owners_result += f"{i},"

    debug_server = input("Enter DEBUG_SERVER id, If there are multiple DEBUG_SERVER, separate them with a comma : ")
    debug_server = set(int(x) for x in debug_server.split(','))
    debug_server_result = ""
    for i in debug_server:
        debug_server_result += f"{i},"

    bot_name = input("Enter your bot name : ")
    bot_tag = input("Enter your bot tag : ").replace("#", "")
    bot_tag = re.sub(r'[^0-9]', '', bot_tag)
    bot_id = int(input("Enter your bot id : "))
    about_bot = input("Enter a description for your bot : ")

    com_psw = input("Enter your computer's password : ")

    file = open("musicbot/config.py", "w", encoding='UTF-8')
    file.write(f'''from musicbot.sample_config import Config

class Development(Config):

    TOKEN = "{token}"
    OWNERS = [{owners_result}]
    DEBUG_SERVER = [{debug_server_result}]
    BOT_NAME = "{bot_name}"
    BOT_TAG = "#{bot_tag}"
    BOT_ID = {bot_id}
    ABOUT_BOT = f"""{about_bot}"""

    # Music
    PSW = "{com_psw}"''')
    file.close()

    print("Config file creation success")
