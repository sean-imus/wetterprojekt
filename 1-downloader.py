import requests
import re
from pathlib import Path

output_dir = "Wetterdaten"
url = "https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/"

if Path(output_dir).exists():
    print(f"{output_dir} Ordner existiert bereits, um Dateien erneut herunterzuladen, bitte Ordner löschen")
    exit()

Path(output_dir).mkdir()

print("Dateien werden heruntergeladen...")

try:
    entire_page = requests.get(url, timeout=30).text
except requests.RequestException as e:
    print(f"Fehler beim Abrufen der Seite: {e}")
    exit()

files = re.findall(r'href="([^"]+(?:zip|txt))"', entire_page)

for i, file in enumerate(files, 1):
    print(f"Downloading ({i}/{len(files)}): {file}")
    try:
        response = requests.get(url + file, timeout=60)
        response.raise_for_status()
        with open(Path(output_dir) / file, "wb") as f:
            f.write(response.content)
    except requests.RequestException as e:
        print(f"Fehler beim Herunterladen von {file}: {e}")
        continue

print("Dateien heruntergeladen!")