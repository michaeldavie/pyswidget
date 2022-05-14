import requests
import asyncio

url = "https://10.123.45.1/network"

payload={"ssid": "havemyownwifi", "password": "MPwPhwZDJD3FynH2peWYDWDGNdLwY9wX", "secretKey": "letmein23"}
payload = "{\r\n    \"ssid\":\"havemyownwifi\",\r\n    \"password\":\"MPwPhwZDJD3FynH2peWYDWDGNdLwY9wX\",\r\n    \"secretKey\":\"letmein23\"\r\n}"
headers = {
  'x-secret-key': 'letmein23'
}

response = requests.request("POST", url, data=payload, verify=False)
print(response.text)


response = requests.request("GET", "https://10.123.45.1/network", headers=headers, verify=False)
print(response.text)

