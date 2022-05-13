#!/usr/bin/env python3
import asyncio
import json


from pyswidget.device import SwidgetDevice
from pyswidget.discovery import discover_devices

SECRET_KEY = "letmein23"
device_addresses = [('24a16074ca14', '192.168.1.143')]

VERIFY_TLS = False


async def main():
    #    device_addresses = await discover_devices()

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
    print(vars(target.assemblies['insert']))
    print(target.hw_info())
    print(target.features)
    # print(target.__dict__)
    # print(target.__dict__['assemblies']['host'].__dict__)
    # print(target.__dict__['assemblies']['insert'].__dict__)
    # print()
    # if target.assemblies["host"].components["0"].functions["toggle"]["state"] == "on":
    #     await target.send_command(
    #         assembly="host", component="0", function="toggle", command={"state": "off"}
    #     )
    #     print("Outlet toggled off")
    # else:
    #     await target.send_command(
    #         assembly="host", component="0", function="toggle", command={"state": "on"}
    #     )
    #     print("Outlet toggled on")

    pass

    for d in devices.values():
        await d._session.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
