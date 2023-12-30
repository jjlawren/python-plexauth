"""Handle a Plex.tv authorization flow to obtain an access token."""

import urllib.parse
import uuid
from asyncio import sleep
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import aiohttp

__version__ = "0.0.5"

CODES_URL = "https://plex.tv/api/v2/pins.json?strong=true"
AUTH_URL = "https://app.plex.tv/auth#!?{}"
TOKEN_URL = "https://plex.tv/api/v2/pins/{}"


class PlexAuth:
    def __init__(
        self,
        payload: Dict[str, str],
        session: Optional[aiohttp.ClientSession] = None,
        headers: Any = None,
    ):
        """Create PlexAuth instance."""
        self.client_identifier = str(uuid.uuid4())
        self._code = None
        self._headers = headers
        self._identifier = None
        self._payload = payload
        self._payload["X-Plex-Client-Identifier"] = self.client_identifier

        self._local_session = False
        if session is None:
            session = aiohttp.ClientSession()
            self._local_session = True
        self._session = session

    async def initiate_auth(self):
        """Request codes needed to create an auth URL.
        Starts external timeout.
        """
        async with self._session.post(
            CODES_URL, data=self._payload, headers=self._headers
        ) as resp:
            response = await resp.json()
            self._code = response["code"]
            self._identifier = response["id"]

    def auth_url(self, forward_url: Optional[str] = None):
        """Return an auth URL for the user to follow."""
        parameters = {
            "clientID": self.client_identifier,
            "code": self._code,
        }
        if forward_url:
            parameters["forwardUrl"] = forward_url

        url = AUTH_URL.format(urllib.parse.urlencode(parameters))
        return url

    async def request_auth_token(self):
        """Request an auth token from Plex."""
        payload = dict(self._payload)
        payload["Accept"] = "application/json"
        async with self._session.get(
            TOKEN_URL.format(self._identifier), headers=payload
        ) as resp:
            response = await resp.json()
            token: str = response["authToken"]
            return token

    async def token(self, timeout: int = 60):
        """Poll Plex endpoint until a token is retrieved or times out."""
        token = None
        wait_until = datetime.now() + timedelta(seconds=timeout)
        break_loop = False
        while not break_loop:
            await sleep(3)
            token = await self.request_auth_token()
            if token or wait_until < datetime.now():
                break_loop = True

        return token

    async def close(self):
        """Close open client session."""
        if self._local_session:
            await self._session.close()

    async def __aenter__(self):
        """Async enter."""
        return self

    async def __aexit__(self, *_):
        """Async exit."""
        await self.close()
