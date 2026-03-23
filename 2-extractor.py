import zipfile
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import os

output_folder = "Extrahierte_Wetterdaten"

def extract_zip(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(output_folder)
    return zip_file.name

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    
    zip_folder = "Wetterdaten"
    
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
    
    worker_count = os.cpu_count()
    with ProcessPoolExecutor(max_workers=worker_count) as executor:
        futures = {executor.submit(extract_zip, z): z for z in zip_files}
        for future in as_completed(futures):
            name = future.result()
            print(f"{name} extrahiert!")
    
    print(f"{len(zip_files)} Dateien extrahiert!")
