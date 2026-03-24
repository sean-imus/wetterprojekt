import sqlite3
import csv
from pathlib import Path

db_file = "wetter.db"
data_folder = "Extrahierte_Wetterdaten"

if not Path(data_folder).exists():
    print(f"{data_folder} Ordner existiert nicht, bitte zuerst 2-extractor.py ausführen")
    exit()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM tbl_messwerte")
if cursor.fetchone()[0] > 0:
    print("Daten existieren bereits in der Datenbank, um Daten erneut zu importieren, bitte 3-create_db.py ausführen")
    exit()
conn.close()

csv_files = list(Path(data_folder).glob("**/produkt_klima_tag_*.txt"))
if not csv_files:
    print(f"Keine CSV Dateien gefunden in {data_folder}, bitte zuerst 2-extractor.py ausführen")
    exit()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

count = 0
for csv_file in csv_files:
    with open(csv_file, "r") as f:
        reader = csv.reader(f, delimiter=";", skipinitialspace=True)
        header = next(reader)
        
        if header[-1].lower() == "eor":
            header = header[:-1]
        
        columns = ",".join(header)
        placeholders = ",".join(["?"] * len(header))
        insert_sql = f"INSERT INTO tbl_messwerte ({columns}) VALUES ({placeholders})"
        
        for row in reader:
            row = [cell.strip() for cell in row]
            if row and row[-1].lower() == "eor":
                row = row[:-1]
            if not row:
                continue
            cursor.execute(insert_sql, row)
        
        conn.commit()
        count += 1
        print(f"{csv_file.name} importiert!")

conn.close()
print(f"{count} .csv Dateien importiert!")
