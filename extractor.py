import zipfile
import re
from pathlib import Path

zip_folder = "Wetterdaten"
output_folder = "Wetterdaten_extracted"

if Path(output_folder).exists():
    print("Ordner für extrahierte Wetterdaten existiert bereits, um Dateien erneut zu extrahieren, bitte Ordner löschen")
    exit()

Path(output_folder).mkdir()

zip_files = Path(zip_folder).glob("*.zip")

for zip_file in zip_files:
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(output_folder)

print("Done!")
