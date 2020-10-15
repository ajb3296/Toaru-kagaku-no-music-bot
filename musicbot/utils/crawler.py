import aiohttp
import json

async def getReqJSON (url : str) :
    async with aiohttp.ClientSession () as session:
      async with session.get (url) as r :
        data = await r.read()
      return json.loads(data)

async def getReqTEXT (url : str, header : str = None) :
    if not header:
        async with aiohttp.ClientSession () as session:
            async with session.get (url = url) as r :
                data = await r.text()
            return data
    async with aiohttp.ClientSession (headers=header) as session:
        async with session.get (url = url) as r :
            data = await r.text()
        return data

async def getReq (url : str, header : str = None) :
    if not header:
        async with aiohttp.ClientSession () as session:
            async with session.get (url) as r :
                return r
    async with aiohttp.ClientSession (headers=header) as session:
        async with session.get (url) as r :
            return r
         
async def checkDevice (device : str) :
    data = await getReqJSON ('https://raw.githubusercontent.com/LineageOS/hudson/master/updater/devices.json')
    for x in data :
        if device in x["model"] :
            return x
    return False
