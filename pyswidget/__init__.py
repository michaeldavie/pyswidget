#!/usr/bin/env python3
import asyncio

import aiohttp
from dotenv import dotenv_values

from discovery import discover_inserts

SECRET_KEY = dotenv_values(".env")["SECRET_KEY"]
VERIFY_TLS = False


class SwidgetInsert:
    def __init__(self, session, addresses):
        self.session = session
        self.mac_address, self.ip_address = addresses

    async def get_summary(self):
        async with self.session.get(
            url=f"https://{self.ip_address}/api/v1/summary", ssl=VERIFY_TLS
        ) as response:
            self.summary = await response.json()

    async def get_state(self):
        async with self.session.get(
            url=f"https://{self.ip_address}/api/v1/state", ssl=VERIFY_TLS
        ) as response:
            self.state = await response.json()


async def main():
    inserts = []
    insert_addresses = await discover_inserts()

    headers = {"x-secret-key": SECRET_KEY}
    connector = aiohttp.TCPConnector(force_close=True)

    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        inserts = [
            SwidgetInsert(session=session, addresses=i) for i in insert_addresses
        ]
        for i in inserts:
            await i.get_state()
            await i.get_summary()

        pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
