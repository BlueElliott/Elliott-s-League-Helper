"""
LCU (League Client Update) Connector
Handles connection to the League of Legends client
"""

import os
import re
import base64
import psutil
import aiohttp
import ssl
from typing import Optional, Tuple
from pathlib import Path


class LCUConnector:
    """Manages connection to the League Client API"""

    def __init__(self):
        self.port: Optional[int] = None
        self.token: Optional[str] = None
        self.base_url: Optional[str] = None
        self.auth_header: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None

    async def connect(self) -> bool:
        """
        Attempt to connect to the League client
        Returns True if successful, False otherwise
        """
        credentials = self._find_lcu_credentials()
        if not credentials:
            return False

        self.port, self.token = credentials
        self.base_url = f"https://127.0.0.1:{self.port}"

        # Create auth header (username is always "riot")
        auth_string = f"riot:{self.token}"
        encoded = base64.b64encode(auth_string.encode()).decode()
        self.auth_header = f"Basic {encoded}"

        # Create aiohttp session with SSL verification disabled
        # (League client uses self-signed certificate)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(connector=connector)

        # Verify connection works
        try:
            async with self.session.get(
                f"{self.base_url}/lol-summoner/v1/current-summoner",
                headers={"Authorization": self.auth_header}
            ) as response:
                if response.status == 200:
                    return True
        except Exception:
            await self.disconnect()
            return False

        return False

    async def disconnect(self):
        """Close the connection"""
        if self.session:
            await self.session.close()
            self.session = None

    def _find_lcu_credentials(self) -> Optional[Tuple[int, str]]:
        """
        Find LCU port and auth token from running League client process
        Returns (port, token) or None if not found
        """
        # Try lockfile method first (most reliable)
        lockfile_creds = self._read_lockfile()
        if lockfile_creds:
            return lockfile_creds

        # Fallback to process command line
        return self._read_from_process()

    def _read_lockfile(self) -> Optional[Tuple[int, str]]:
        """
        Read credentials from lockfile
        Located at: C:/Riot Games/League of Legends/lockfile
        """
        possible_paths = [
            Path("C:/Riot Games/League of Legends/lockfile"),
            Path.home() / "Riot Games/League of Legends/lockfile",
        ]

        for lockfile_path in possible_paths:
            if lockfile_path.exists():
                try:
                    with open(lockfile_path, 'r') as f:
                        content = f.read()

                    # Format: LeagueClient:PID:PORT:TOKEN:PROTOCOL
                    parts = content.split(':')
                    if len(parts) >= 4:
                        port = int(parts[2])
                        token = parts[3]
                        return (port, token)
                except Exception:
                    continue

        return None

    def _read_from_process(self) -> Optional[Tuple[int, str]]:
        """
        Read credentials from LeagueClientUx process command line
        Fallback method if lockfile is not accessible
        """
        try:
            for process in psutil.process_iter(['name', 'cmdline']):
                if process.info['name'] in ['LeagueClientUx.exe', 'LeagueClient.exe']:
                    cmdline = ' '.join(process.info['cmdline'])

                    # Extract port
                    port_match = re.search(r'--app-port=(\d+)', cmdline)
                    # Extract token
                    token_match = re.search(r'--remoting-auth-token=([\w-]+)', cmdline)

                    if port_match and token_match:
                        port = int(port_match.group(1))
                        token = token_match.group(1)
                        return (port, token)
        except Exception:
            pass

        return None

    async def request(self, method: str, endpoint: str, **kwargs) -> Optional[dict]:
        """
        Make a request to the LCU API

        Args:
            method: HTTP method (GET, POST, DELETE, etc.)
            endpoint: API endpoint (e.g., '/lol-perks/v1/pages')
            **kwargs: Additional arguments to pass to aiohttp request

        Returns:
            Response JSON or None if request failed
        """
        if not self.session or not self.base_url:
            return None

        url = f"{self.base_url}{endpoint}"
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = self.auth_header

        try:
            async with self.session.request(method, url, headers=headers, **kwargs) as response:
                if response.status in [200, 201, 204]:
                    if response.status == 204:  # No content
                        return {}
                    return await response.json()
                else:
                    return None
        except Exception:
            return None

    async def get(self, endpoint: str, **kwargs) -> Optional[dict]:
        """GET request wrapper"""
        return await self.request('GET', endpoint, **kwargs)

    async def post(self, endpoint: str, **kwargs) -> Optional[dict]:
        """POST request wrapper"""
        return await self.request('POST', endpoint, **kwargs)

    async def delete(self, endpoint: str, **kwargs) -> Optional[dict]:
        """DELETE request wrapper"""
        return await self.request('DELETE', endpoint, **kwargs)

    async def put(self, endpoint: str, **kwargs) -> Optional[dict]:
        """PUT request wrapper"""
        return await self.request('PUT', endpoint, **kwargs)
