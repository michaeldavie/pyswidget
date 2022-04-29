#!/usr/bin/env python3
import asyncio

from dotenv import dotenv_values

from devices import SwidgetDevice
from discovery import discover_inserts

SECRET_KEY = dotenv_values(".env")["SECRET_KEY"]
VERIFY_TLS = False

inserts = []


async def main():
    insert_addresses = await discover_inserts()

    inserts = [
        SwidgetDevice(addresses=i, secret_key=SECRET_KEY, ssl=VERIFY_TLS)
        for i in insert_addresses
    ]

    for i in inserts:
        await i.get_summary()
        await i.get_state()

    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
