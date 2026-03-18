import requests
import re
from pathlib import Path

DATA_DIR = "Wetterdaten"
url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/"

if Path(DATA_DIR).exists():
    print("Wetterdaten Ordner existiert bereits, um Dateien erneut herunterzuladen, bitte Ordner löschen")
    exit()

Path(DATA_DIR).mkdir()

entire_page = requests.get(url).text
files = re.findall(r'href="([^"]+\.(?:zip|txt))"', entire_page)

for file in files:
    data = requests.get(url + file).content
    open(Path(DATA_DIR) / file, "wb").write(data)

print(f"Downloaded {len(files)} files!")
