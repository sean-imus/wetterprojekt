import zipfile
from pathlib import Path

zip_folder = "Wetterdaten"
output_folder = "Wetterdaten_extracted"

if not Path(zip_folder).exists():
    print(f"Ordner {zip_folder} existiert nicht, bitte zuerst downloader.py ausführen")
    exit()

if Path(output_folder).exists():
    print("Ordner für extrahierte Wetterdaten existiert bereits, um Dateien erneut zu extrahieren, bitte Ordner löschen")
    exit()

Path(output_folder).mkdir()

zip_files = list(Path(zip_folder).glob("*.zip"))
if not zip_files:
    print(f"Keine zip Dateien gefunden in {zip_folder}, zuerst downloader.py ausführen")
    exit()

total = len(zip_files)
print(f"Extracting {total} files:")

for i, zip_file in enumerate(zip_files, 1):
    print(f"Extracting {i}/{total}: {zip_file.name}")
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(output_folder)

print(f"Done! Extracted {total} files.")
