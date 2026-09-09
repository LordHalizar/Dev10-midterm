import requests

API_URL = "https://api.census.gov/data/"
API_KEY = "e790743a691c8fdc19dd130bbd807f4fe692dd82"

params = {
    "get": "NAME,B01001_001E",
    "for": "us:*",
    "key": API_KEY
}
years = ["2021", "2022", "2023", "2024"]
# class PopulationAPI:
#     _key = "e790743a691c8fdc19dd130bbd807f4fe692dd82"

#     def __init__(self, url):
#         self._url = url
data = {}
for year in years:
    url = f"{API_URL}{year}/acs/acs1"
    response = requests.get(url, params=params)
    print(response.status_code)
    if response.status_code == 200:
        print(response.url)
        data[year] = response.json()
# print(response.status_code)
# print(response.headers.get("Content-Type"))
# print(response.text[:500]) 
# print(response.url)
# print(response.json())

for year, result in data.items():
    print(f"Data for {year}: {result}")

