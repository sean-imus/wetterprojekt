import sqlite3
from pathlib import Path

DB_NAME = "wetter.db"
DATA_DIR = "Extrahierte_Wetterdaten"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM tbl_messwerte")
if cursor.fetchone()[0] > 0:
    print("Daten existieren bereits in der Datenbank, um Daten erneut zu importieren, lösche die Datenbank und führe create_db.py aus")
    exit()

conn.close()

csv_files = list(Path(DATA_DIR).glob("**/produkt_klima_tag_*.txt"))
if not csv_files:
    print(f"Keine csv Dateien gefunden in {DATA_DIR}, nicht vergessen zuerst extractor.py auszuführen")
    exit()

print(f"Found {len(csv_files)} CSV files")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for csv_file in csv_files:
    print(f"Processing {csv_file.name}...")
    with open(csv_file, "r") as f:
        lines = f.readlines()
    
    header = lines[0].strip().split(";")[:-1]
    
    for line in lines[1:]:
        values = line.strip().split(";")[:-1]
        placeholders = ",".join(["?"] * len(values))
        cursor.execute(f"INSERT INTO tbl_messwerte ({','.join(header)}) VALUES ({placeholders})", values)

conn.commit()
conn.close()
print("Done!")
