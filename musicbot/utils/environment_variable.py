import os

class EnV:
    def __init__(self):
        self.env_bot = "TKBOT_HOME"
    
    def get_bot_env(self) -> str | None:
        """ 대시보드 사용시 필요한 봇 환경변수 가져오기 """
        return os.environ.get(self.env_bot)
    
    def set_bot_env(self) -> None:
        """ 현재 경로를 환경변수에 할당, 대시보드 사용시 필요 """
        os.environ[self.env_bot] = os.getcwd()