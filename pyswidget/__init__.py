#!/usr/bin/env python3
import asyncio
from time import sleep

from dotenv import dotenv_values
import requests

from discovery import discover_inserts

SECRET_KEY = dotenv_values(".env")["SECRET_KEY"]
VERIFY_TLS = False


class SwidgetInsert:
    def __init__(self, addresses: tuple) -> None:
        self.mac_address, self.ip_address = addresses

        self.session = requests.session()
        self.session.headers = {"x-secret-key": SECRET_KEY}
        self.session.verify = VERIFY_TLS

        self.summary = self.session.get(
            url=f"https://{self.ip_address}/api/v1/summary"
        ).json()
        sleep(0.5)
        self.update_state()

    def update_state(self):
        self.state = self.session.get(
            url=f"https://{self.ip_address}/api/v1/state"
        ).json()


async def main():
    if not VERIFY_TLS:
        requests.packages.urllib3.disable_warnings()

    insert_addresses = await discover_inserts()

    inserts = [SwidgetInsert(addresses=i) for i in insert_addresses]

    pass


if __name__ == "__main__":
    asyncio.run(main())
