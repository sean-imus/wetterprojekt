import zipfile
from pathlib import Path

zip_folder = "Wetterdaten"
output_folder = "Extrahierte_Wetterdaten"

if not Path(zip_folder).exists():
    print(f"{output_folder} Ordner existiert nicht, bitte zuerst 1-downloader.py ausführen")
    exit()

if Path(output_folder).exists():
    print(f"{output_folder} Ordner existiert bereits, um Dateien erneut zu extrahieren, bitte Ordner löschen")
    exit()

Path(output_folder).mkdir()

zip_files = list(Path(zip_folder).glob("*.zip"))
if not zip_files:
    print(f"Keine .zip Dateien gefunden in {zip_folder}, bitte zuerst 1-downloader.py ausführen")
    exit()

count = 0
for zip_file in zip_files:
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(output_folder)
    count += 1
    print(f"{zip_file.name} extrahiert!")

print(f"{count} Dateien extrahiert!")
