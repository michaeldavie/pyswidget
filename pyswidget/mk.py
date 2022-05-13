import requests
import asyncio

url = "https://192.168.1.143/api/v1/state"

payload={}
headers = {
  'x-secret-key': 'letmein23'
}

response = requests.request("GET", url, headers=headers, data=payload, verify=False)

from pprint import pprint
print("STATE")
pprint(response.json())

url = "https://192.168.1.143/api/v1/summary"
response = requests.request("GET", url, headers=headers, data=payload, verify=False)
print("SUMMRY")
pprint(response.json())


from device import SwidgetDevice
from swidgetoutlet import SwidgetOutlet
async def main():

  a = SwidgetOutlet('192.168.1.143', 'letmein23', False)
  print(a)
  await a.update()
  await a.turn_off()
  print(await(a.total_consumption()))
  print(await(a.get_plug_comsumption(0)))
  print(a.get_function_values('aq'))
  print(a.get_sensor_value('aq', 'iaq'))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
