#!/usr/bin/env python3
import asyncio
import json

from dotenv import dotenv_values

from pyswidget.devices import SwidgetDevice
from pyswidget.discovery import discover_devices

ENV_VALUES = dotenv_values(".env")
SECRET_KEY = ENV_VALUES["SECRET_KEY"]

VERIFY_TLS = False

off_command = {"host": {"components": {"0": {"toggle": {"state": "off"}}}}}
on_command = {"host": {"components": {"0": {"toggle": {"state": "on"}}}}}


async def main():
    #    device_addresses = await discover_devices()
    device_addresses = json.loads(ENV_VALUES["ADDRESSES"])

    devices = {
        device[0]: SwidgetDevice(
            addresses=device, secret_key=SECRET_KEY, ssl=VERIFY_TLS
        )
        for device in device_addresses
    }

    for d in devices.values():
        await d.get_summary()
        await d.get_state()

    target = devices["500291a25ff0"]
    if target.assemblies["host"].components["0"].toggle == "on":
        await target.send_command(data=off_command)
    else:
        await target.send_command(data=on_command)

    pass

    for d in devices.values():
        await d.session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
