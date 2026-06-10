import requests
import re
from pathlib import Path

output_dir = "Wetterdaten"
url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/"

if Path(output_dir).exists():
    print(
        f"{output_dir} Ordner existiert bereits, um Dateien erneut herunterzuladen, bitte Ordner löschen"
    )
    exit()

Path(output_dir).mkdir()

print("Seite wird abgerufen...")
seite = requests.get(url, timeout=30).text
dateien = re.findall(r'href="([^"]+(?:zip|txt))"', seite)

print("Dateien werden heruntergeladen...")
for datei in dateien:
    antwort = requests.get(url + datei, timeout=60)
    with open(Path(output_dir) / datei, "wb") as f:
        f.write(antwort.content)

print("Dateien heruntergeladen!")
