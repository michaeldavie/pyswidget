#!/usr/bin/env python3
import asyncio
import json

from dotenv import dotenv_values

from pyswidget.devices import SwidgetDevice
from pyswidget.discovery import discover_devices

ENV_VALUES = dotenv_values(".env")
SECRET_KEY = ENV_VALUES["SECRET_KEY"]

VERIFY_TLS = False

inserts = []


async def main():
    #    device_addresses = await discover_devices()
    device_addresses = json.loads(ENV_VALUES["ADDRESSES"])

    devices = [
        SwidgetDevice(addresses=i, secret_key=SECRET_KEY, ssl=VERIFY_TLS)
        for i in device_addresses
    ]

    for i in devices:
        await i.get_summary()
        await i.get_state()

    pass


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
