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
    columns = ",".join(header)
    placeholders = ",".join(["?"] * len(header))
    insert_sql = f"INSERT INTO tbl_messwerte ({columns}) VALUES ({placeholders})"
    
    rows = [line.strip().split(";")[:-1] for line in lines[1:]]
    cursor.executemany(insert_sql, rows)
    conn.commit()
    print(f"{csv_file.name} importiert!")

conn.close()
print(f"{len(csv_files)} .csv Dateien importiert!")
