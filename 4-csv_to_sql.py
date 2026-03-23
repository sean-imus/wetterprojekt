import sqlite3
from pathlib import Path

db_file = "wetter.db"
data_folder = "Extrahierte_Wetterdaten"

if not Path(data_folder).exists():
    print(f"{data_folder} Ordner existiert nicht, bitte zuerst extractor.py ausführen")
    exit()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM tbl_messwerte")
if cursor.fetchone()[0] > 0:
    print("Daten existieren bereits in der Datenbank, um Daten erneut zu importieren, bitte create_db.py ausführen")
    exit()

conn.close()

csv_files = list(Path(data_folder).glob("**/produkt_klima_tag_*.txt"))
if not csv_files:
    print(f"Keine CSV Dateien gefunden in {data_folder}, bitte zuerst extractor.py ausführen")
    exit()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

for csv_file in csv_files:
    with open(csv_file, "r") as f:
        lines = f.readlines()
    
    header = lines[0].strip().split(";")[:-1]
    
    for line in lines[1:]:
        values = line.strip().split(";")[:-1]
        placeholders = ",".join(["?"] * len(values))
        cursor.execute(f"INSERT INTO tbl_messwerte ({','.join(header)}) VALUES ({placeholders})", values)
    print(f"{csv_file.name} importiert!")

conn.commit()
conn.close()
print(f"{len(csv_files)} .csv Dateien importiert!")
