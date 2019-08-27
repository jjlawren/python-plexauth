"""Handle a Plex.tv authorization flow to obtain an access token."""
import aiohttp
from asyncio import sleep
from datetime import datetime, timedelta
import urllib.parse
import uuid

__version__ = '0.0.1'

CODES_URL = 'https://plex.tv/api/v2/pins.json?strong=true'
AUTH_URL = 'https://app.plex.tv/auth#!?{}'
TOKEN_URL = 'https://plex.tv/api/v2/pins/{}'

class PlexAuth():

    def __init__(self, payload):
        '''Create PlexAuth instance.'''
        self._client_identifier = str(uuid.uuid4())
        self._code = None
        self._identifier = None
        self._payload = payload
        self._payload['X-Plex-Client-Identifier'] = self._client_identifier

    async def initiate_auth(self):
        '''Request codes needed to create an auth URL. Starts external timeout.'''
        async with aiohttp.ClientSession() as session:
            async with session.post(CODES_URL, data=self._payload) as resp:
                response = await resp.json()
                self._code = response['code']
                self._identifier = response['id']

    def auth_url(self, forward_url=None):
        '''Return an auth URL for the user to follow.'''
        parameters = {
            'clientID': self._client_identifier,
            'code': self._code,
        }
        url = AUTH_URL.format(urllib.parse.urlencode(parameters))
        return url

    async def request_auth_token(self):
        '''Request an auth token from Plex.'''
        token_url = TOKEN_URL.format(self._code)
        async with aiohttp.ClientSession() as session:
            payload = dict(self._payload)
            payload['Accept'] = 'application/json'
            async with session.get(TOKEN_URL.format(self._identifier), headers=payload) as resp:
                response = await resp.json()
                token = response['authToken']
                return token

    async def token(self, timeout=60):
        '''Poll Plex endpoint until a token is retrieved or times out.'''
        token = None
        wait_until = datetime.now() + timedelta(seconds=timeout)
        break_loop = False
        while not break_loop:
            await sleep(3)
            token = await self.request_auth_token()
            if token or wait_until < datetime.now():
                break_loop = True

        return token
