import requests
import re
from pathlib import Path

output_folder = "Wetterdaten"
url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/"

if Path(output_folder).exists():
    print(f"{output_folder} Ordner existiert bereits, um Dateien erneut herunterzuladen, bitte Ordner löschen")
    exit()

Path(output_folder).mkdir()

print("Dateien werden heruntergeladen...")

entire_page = requests.get(url).text
files = re.findall(r'href="([^"]+\.(?:zip|txt))"', entire_page)

for file in files:
    data = requests.get(url + file).content
    open(Path(output_folder) / file, "wb").write(data)

print("Dateien heruntergeladen!")
