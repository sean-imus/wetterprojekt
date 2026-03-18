import requests
import re

url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/"

entire_page = requests.get(url).text
files = re.findall(r'href="([^"]+\.(?:zip|txt))"', entire_page)

for file in files:
    print(file)
