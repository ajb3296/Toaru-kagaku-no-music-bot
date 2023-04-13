import aiohttp
import json

connector = aiohttp.TCPConnector(verify_ssl=False)

async def getReqJSON(url: str):
    async with aiohttp.ClientSession() as session:
      async with session.get(url) as r:
        data = await r.read()
      return json.loads(data)

async def getReqTEXT(url: str, header:(dict | None) = None) -> str:
    if header is None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url = url) as r:
                data = await r.text()
            return data
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(url = url) as r:
            data = await r.text()
        return data

async def getReq(url: str, header:(dict | None) = None):
    if header is None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as r:
                return r
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(url) as r:
            return r
