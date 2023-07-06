import time

from musicbot.utils.statistics import StatisticsDb
from musicbot.utils.ytdata import YTData

from datetime import datetime


def update_cache_process():
    """ 캐시 업데이트 프로세스, 밤 11시 0분(23시 0분)에 캐시 미리 업데이트 """

    yd = YTData()
    sdb = StatisticsDb()
    now = datetime.now()

    print("START UPDATE CACHE PROCESS")

    while True:
        # 지금 시간이 밤 11시면
        if (now.hour == 23) and (now.minute == 0):
            # 데이터 가져오기
            today_data = sdb.get_all(f"date{now.strftime('%Y%m%d')}")
            if today_data is not None:
                for data in today_data:
                    _, video_id, _ = data
                    # 데이터 업데이트
                    yd.get(video_id)

        time.sleep(60)