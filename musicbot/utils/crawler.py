import aiohttp
import json

async def getReqJSON(url: str):
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as r:
            data = await r.read()
        return json.loads(data)


async def getReqTEXT(url: str, header: (dict | None) = None) -> str:
    connector = aiohttp.TCPConnector(ssl=False)
    if header is None:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url=url) as r:
                data = await r.text()
            return data
    async with aiohttp.ClientSession(connector=connector, headers=header) as session:
        async with session.get(url=url) as r:
            data = await r.text()
        return data


async def getReq(url: str, header: (dict | None) = None):
    connector = aiohttp.TCPConnector(ssl=False)
    if header is None:
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as r:
                return r
    async with aiohttp.ClientSession(connector=connector, headers=header) as session:
        async with session.get(url) as r:
            return r