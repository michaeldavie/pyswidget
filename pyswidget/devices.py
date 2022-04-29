import json

from aiohttp import ClientSession, TCPConnector


class SwidgetDevice:
    def __init__(self, addresses, secret_key, ssl):
        self.mac_address, self.ip_address = addresses
        self.ssl = ssl
        headers = {"x-secret-key": secret_key}
        connector = TCPConnector(force_close=True)
        self.session = ClientSession(headers=headers, connector=connector)

    async def get_summary(self):
        async with self.session.get(
            url=f"https://{self.ip_address}/api/v1/summary", ssl=self.ssl
        ) as response:
            summary = await response.json()

        self.model = summary["model"]
        self.version = summary["version"]
        self.assemblies = {
            "host": HostAssembly(summary["host"]),
            "insert": InsertAssembly(summary["insert"]),
        }

    async def get_state(self):
        async with self.session.get(
            url=f"https://{self.ip_address}/api/v1/state", ssl=self.ssl
        ) as response:
            state = await response.json()

        self.rssi = state["connection"]["rssi"]

        for assembly in self.assemblies:
            for id, component in self.assemblies[assembly].components.items():
                component.functions = state[assembly]["components"][id]

    async def send_command(
        self, assembly: str, component: str, function: str, command: dict
    ):
        data = json.dumps({assembly: {"components": {component: {function: command}}}})

        async with self.session.post(
            url=f"https://{self.ip_address}/api/v1/command",
            ssl=self.ssl,
            data=data,
        ) as response:
            state = await response.json()

        function_value = state[assembly]["components"][component][function]
        self.assemblies[assembly].components[component].functions[function] = function_value  # fmt: skip


class HostAssembly:
    def __init__(self, summary):
        self.id = summary["id"]
        self.type = summary["type"]
        self.error = summary["error"]
        self.components = {
            c["id"]: SwidgetComponent(c["functions"]) for c in summary["components"]
        }


class InsertAssembly:
    def __init__(self, summary):
        self.type = summary["type"]
        self.components = {
            c["id"]: SwidgetComponent(c["functions"]) for c in summary["components"]
        }


class SwidgetComponent:
    def __init__(self, functions):
        self.functions = {f: None for f in functions}
