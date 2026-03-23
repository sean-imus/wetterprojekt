import sqlite3
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

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

def parse_and_insert(csv_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    with open(csv_file, "r") as f:
        lines = f.readlines()
    
    header = lines[0].strip().split(";")[:-1]
    columns = ",".join(header)
    placeholders = ",".join(["?"] * len(header))
    insert_sql = f"INSERT INTO tbl_messwerte ({columns}) VALUES ({placeholders})"
    
    batch_size = 5000
    for i in range(1, len(lines), batch_size):
        batch = [line.strip().split(";")[:-1] for line in lines[i:i+batch_size]]
        cursor.executemany(insert_sql, batch)
        conn.commit()
    
    conn.close()
    return csv_file.name

worker_count = os.cpu_count()
with ThreadPoolExecutor(max_workers=worker_count) as executor:
    futures = {executor.submit(parse_and_insert, csv): csv for csv in csv_files}
    for future in as_completed(futures):
        name = future.result()
        print(f"{name} importiert!")

print(f"{len(csv_files)} .csv Dateien importiert!")
