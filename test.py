#!/usr/bin/env python3
import asyncio
import json

from dotenv import dotenv_values

from pyswidget.devices import SwidgetDevice
from pyswidget.discovery import discover_devices

ENV_VALUES = dotenv_values(".env")
SECRET_KEY = ENV_VALUES["SECRET_KEY"]

VERIFY_TLS = False


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

    target = devices[device_addresses[0][0]]
    if target.assemblies["host"].components["0"].functions["toggle"]["state"] == "on":
        await target.send_command(
            assembly="host", component="0", function="toggle", command={"state": "off"}
        )
        print("Outlet toggled off")
    else:
        await target.send_command(
            assembly="host", component="0", function="toggle", command={"state": "on"}
        )
        print("Outlet toggled on")

    pass

    for d in devices.values():
        await d._session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
