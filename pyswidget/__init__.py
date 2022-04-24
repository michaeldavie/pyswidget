#!/usr/bin/env python3
import asyncio
from time import sleep
import socket
from urllib.parse import urlparse

from dotenv import dotenv_values
import requests
import ssdp

SECRET_KEY = dotenv_values(".env")["SECRET_KEY"]
VERIFY_TLS = False

class SwidgetProtocol(ssdp.SimpleServiceDiscoveryProtocol):
    """Protocol to handle responses and requests."""

    insert_addresses = []

    def response_received(self, response: ssdp.SSDPResponse, addr: tuple):
        """Handle an incoming response."""
        headers = {h[0]: h[1] for h in response.headers}
        mac_address = headers["USN"].split("-")[-1]
        ip_address = urlparse(headers["LOCATION"]).hostname
        self.insert_addresses.append((mac_address, ip_address))


def discover_inserts():
    # Start the asyncio loop.
    loop = asyncio.get_event_loop()
    connect = loop.create_datagram_endpoint(SwidgetProtocol, family=socket.AF_INET)
    transport, protocol = loop.run_until_complete(connect)

    # Send out an M-SEARCH request, requesting Swidget service types.
    search_request = ssdp.SSDPRequest(
        "M-SEARCH",
        headers={
            "HOST": "239.255.255.250:1900",
            "MAN": '"ssdp:discover"',
            "MX": "2",
            "ST": "urn:swidget:pico:1",
        },
    )
    search_request.sendto(transport, (SwidgetProtocol.MULTICAST_ADDRESS, 1900))

    # Keep running for 3 seconds.
    try:
        loop.run_until_complete(asyncio.sleep(3))
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()

    inserts = protocol.insert_addresses

    return inserts


class SwidgetInsert():
    
    def __init__(self, addresses: tuple) -> None:
        self.mac_address, self.ip_address = addresses

        self.session = requests.session()
        self.session.headers = {"x-secret-key": SECRET_KEY}
        self.session.verify = VERIFY_TLS

        self.summary = self.session.get(url=f"https://{self.ip_address}/api/v1/summary").json()
        sleep(0.5)
        self.update_state()

    def update_state(self):
        self.state = self.session.get(url=f"https://{self.ip_address}/api/v1/state").json()

if __name__ == "__main__":
    if not VERIFY_TLS:
        requests.packages.urllib3.disable_warnings()

    insert_addresses = discover_inserts()

    inserts = [SwidgetInsert(addresses=i) for i in insert_addresses]

    pass