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
                component.update(state[assembly]["components"][id])

    async def send_command(self, command):
        async with self.session.post(
            url=f"https://{self.ip_address}/api/v1/command", ssl=self.ssl, data={}
        ) as response:
            state = await response.json()


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


class ToggleComponent:
    def __init__(self, state=None):
        self.state = state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value not in ["ON", "OFF"]:
            raise ValueError("Toggle state must be 'ON' or 'OFF'")
        self._state = value


class SwidgetComponent:
    def __init__(self, functions):
        for f in functions:
            if f == "toggle":
                self.toggle = None
            elif f == "power":
                self.current = None
                self.avg = None
                self.avgOn = None
            elif f == "temperature":
                self.temperature = None
            elif f == "humidity":
                self.humidity = None

    def update(self, state: dict):
        for function, value in state.items():
            if function == "toggle":
                self.toggle = value["state"]
            elif function == "power":
                self.current = value["current"]
                self.avg = value["avg"]
                self.avgOn = value["avgOn"]
            elif function == "temperature":
                self.temperature = value["now"]
            elif function == "humidity":
                self.humidity = value["now"]
