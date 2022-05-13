from device import (
    DeviceType,
    SwidgetDevice
)


class SwidgetOutlet(SwidgetDevice):

    def __init__(self, host,  secret_key: str, ssl: bool) -> None:
        super().__init__(host=host, secret_key=secret_key, ssl=ssl)
        self._device_type = DeviceType.Outlet

    async def current_consumption(self) -> float:
        """Get the current power consumption in watts."""
        return sum([await plug.current_consumption() for plug in self.children])

    async def turn_on(self):
        """Turn the device on."""
        await self.send_command(
            assembly="host", component="0", function="toggle", command={"state": "on"}
        )

    async def turn_off(self):
        """Turn the device off."""
        await self.send_command(
            assembly="host", component="0", function="toggle", command={"state": "off"}
        )

    async def total_consumption(self):
        """Get the total power consumption in watts."""
        await self.get_state()
        total_consumption = 0
        for id, properties in self.assemblies['host'].components.items():
            print(vars(properties))
            total_consumption += properties.functions['power']['current']
        return total_consumption

    async def get_plug_comsumption(self, plug_id):
        """Get the power consumption of a plug in watts."""
        return self.assemblies['host'].components[str(plug_id)].functions['power']['current']