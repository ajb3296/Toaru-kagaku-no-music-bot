from bs4 import BeautifulSoup
import billboard

from musicbot.utils.crawler import getReqTEXT

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}


async def get_melon(count = 10):
    melon_url = 'https://www.melon.com/chart/index.htm'
    data = await getReqTEXT (melon_url, header)
    parse = BeautifulSoup(data, 'lxml')
    musics = parse.find_all("tr", {"class" : "lst50"})
    title = []
    artist = []
    for num in range(0, count):
        title.append(musics[num].find("div", {"class" : "ellipsis rank01"}).find("a").text)
        artist.append(musics[num].find("div", {"class" : "ellipsis rank02"}).find("a").text)
    return title, artist

async def get_billboard(count = 10):
    chart = billboard.ChartData('hot-100')
    title = []
    artist = []
    for num in range(0, count):
        title.append(chart[num].title)
        artist.append(chart[num].artist)
    return title, artist

async def get_billboardjp(count = 10):
    billboardjp_url = 'https://www.billboard-japan.com/charts/detail?a=hot100'
    data = await getReqTEXT(billboardjp_url, header)
    parse = BeautifulSoup(data, 'lxml')
    musics = parse.find("tbody").find_all("tr")
    title = []
    artist = []
    for num in range(0, count):
        title.append(musics[num].find("p", {"class" : "musuc_title"}).text)
        artist.append(musics[num].find("p", {"class" : "artist_name"}).text)
    return title, artist