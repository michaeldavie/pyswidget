import asyncio
import socket
from urllib.parse import urlparse

import ssdp

RESPONSE_SEC = 2
SWIDGET_ST = "urn:swidget:pico:1"

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
            "MX": RESPONSE_SEC,
            "ST": SWIDGET_ST,
        },
    )
    search_request.sendto(transport, (SwidgetProtocol.MULTICAST_ADDRESS, 1900))

    # Keep running for response time seconds.
    try:
        loop.run_until_complete(asyncio.sleep(RESPONSE_SEC + 0.5))
    except KeyboardInterrupt:
        pass

    transport.close()
    loop.close()

    return protocol.insert_addresses
