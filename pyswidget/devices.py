from aiohttp import ClientSession, TCPConnector

ASSEMBLIES = ["host", "insert"]


class SwidgetDevice:
    def __init__(self, addresses, secret_key, ssl):
        self.mac_address, self.ip_address = addresses
        self.model = str()
        self.version = str()
        self.host_id = str()
        self.host_type = str()
        self.host_error = int()
        self.insert_type = str()
        self.rssi = int()
        self.components = dict()

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
        self.host_id = summary["host"]["id"]
        self.host_type = summary["host"]["type"]
        self.host_error = summary["host"]["error"]
        self.insert_type = summary["insert"]["type"]

        for assembly in ASSEMBLIES:
            self.components[assembly] = {
                c["id"]: SwidgetComponent(c["functions"])
                for c in summary[assembly]["components"]
            }

    async def get_state(self):
        async with self.session.get(
            url=f"https://{self.ip_address}/api/v1/state", ssl=self.ssl
        ) as response:
            state = await response.json()

        component_states = dict()

        for assembly in ASSEMBLIES:
            component_states[assembly] = state[assembly]["components"]
            for id, component in self.components[assembly].items():
                component.update(component_states[assembly][id])

    async def send_command(self, command):
        async with self.session.post(
            url=f"https://{self.ip_address}/api/v1/command", ssl=self.ssl, data={}
        ) as response:
            state = await response.json()


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
