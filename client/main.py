import aiohttp
import asyncio
import async_timeout
import json
import time
import logging


log = logging.getLogger(__name__)


class RequestData():
    def __init__(self, url, data, loop, endpoint):
        self.url = url
        self.data = data
        self.jwt = None
        self.display = []
        self.loop = loop or asyncio.get_event_loop()
        self.endpoint = endpoint
        self.history = []
        self.preset()

    async def get_auth(self, session):
        if not self.jwt:
            log.info('login...')
            await self.login(session)
            log.info('Login successful！')
        return {'Authorization': 'Bearer {}'.format(self.jwt)}

    async def login(self, session):
        try:
            async with async_timeout.timeout(10):
                async with session.post('{}/auth'.format(self.url),
                                        data=json.dumps(self.data)) as response:
                    res = await response.json()
                    self.jwt = res.get('access_token')
        except OSError:
             log.error('Connection {} failed...'.format(self.url))

    async def get_data(self, session, auth):
        with async_timeout.timeout(10):
            async with session.get('{}/{}'.format(self.url, self.endpoint),
                                   headers=auth) as response:
                return await response.json()

    async def index(self, session):
        with async_timeout.timeout(10):
            async with session.get('{}'.format(self.url)) as response:
                return await response.json()

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            auth = await self.get_auth(session)
            if not auth:
                return
            log.info('load the data...')
            while True:
                try:
                    res = await self.get_data(session, auth)
                    if "reasons" in res:
                        self.jwt = None
                        auth = await self.get_auth(session)

                    if len(self.display) >= 10:
                        self.display.pop(0)
                    self.display.append(res)

                    self.grep_alarm(res)

                except Exception as e:
                    log.error('error: {}'.format(e))

    def grep_alarm(self, res):
        _alarm = []
        if self.history == []:
            log.info('v1/events response data is: {}'.format(res))
        for i in range(len(res)):
            if res[i] not in self.history:
                _alarm.append(res[i])
        if _alarm != []:
            log.info('New alarm is {}'.format(_alarm))
        self.history = res

    def preset(self):
        asyncio.ensure_future(self.fetch_data())

    def get_info(self):
        return self.display


if __name__=="__main__":
    loop = asyncio.get_event_loop()

    url = "http://127.0.0.1:8080"
    data = {"username": "user1", "password": "abcxyz"}

    login = RequestData(url, data)
