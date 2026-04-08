import zipfile
from pathlib import Path

zip_dir = "Wetterdaten"
output_dir = "Extrahierte_Wetterdaten"

if not Path(zip_dir).exists():
    print(f"{output_dir} Ordner existiert nicht, bitte zuerst 1-downloader.py ausführen")
    exit()

if Path(output_dir).exists():
    print(f"{output_dir} Ordner existiert bereits, um Dateien erneut zu extrahieren, bitte Ordner löschen")
    exit()

Path(output_dir).mkdir()

zip_files = list(Path(zip_dir).glob("*.zip"))
if not zip_files:
    print(f"Keine .zip Dateien gefunden in {zip_dir}, bitte zuerst 1-downloader.py ausführen")
    exit()

print("Dateien werden extrahiert...")

for zip_file in zip_files:
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(output_dir)

print("Dateien extrahiert!")