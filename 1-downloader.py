import requests
import re
from pathlib import Path

output_folder = "Wetterdaten"
url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/"

if Path(output_folder).exists():
    print(f"{output_folder} Ordner existiert bereits, um Dateien erneut herunterzuladen, bitte Ordner löschen")
    exit()

Path(output_folder).mkdir()

entire_page = requests.get(url).text
files = re.findall(r'href="([^"]+\.(?:zip|txt))"', entire_page)

count = 0
for file in files:
    data = requests.get(url + file).content
    open(Path(output_folder) / file, "wb").write(data)
    count += 1
    print(f"{file} heruntergeladen!")

print(f"{count} Dateien heruntergeladen!")
