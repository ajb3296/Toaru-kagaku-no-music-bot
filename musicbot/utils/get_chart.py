from bs4 import BeautifulSoup
import billboard

from musicbot.utils.crawler import getReqTEXT

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}


async def get_melon(count: int = 10) -> tuple[list, list]:
    """ 멜론 차트 반환 """
    melon_url = 'https://www.melon.com/chart/index.htm'
    data = await getReqTEXT (melon_url, header)
    parse = BeautifulSoup(data, 'lxml')
    musics = parse.find_all("tr", {"class" : "lst50"})
    title = []
    artist = []
    for num in range(0, count):
        try:
            title.append(musics[num].find("div", {"class" : "ellipsis rank01"}).find("a").text)
            artist.append(musics[num].find("div", {"class" : "ellipsis rank02"}).find("a").text)
        except:
            break
    return title, artist

async def get_billboard(count: int = 10) -> tuple[list, list]:
    """ 빌보드 차트 반환 """
    chart = billboard.ChartData('hot-100')
    title = []
    artist = []
    for num in range(0, count):
        try:
            title.append(chart[num].title)
            artist.append(chart[num].artist)
        except:
            pass
    return title, artist

async def get_billboardjp(count: int = 10) -> tuple[list, list]:
    """ 빌보드 재팬 차트 반환 """
    chart = billboard.ChartData('japan-hot-100')
    title = []
    artist = []
    for num in range(0, count):
        try:
            title.append(chart[num].title)
            artist.append(chart[num].artist)
        except:
            pass
    return title, artist