import sqlite3
import csv
from pathlib import Path

db_path = "wetter.db"
data_dir = "Extrahierte_Wetterdaten"
station_file_path = "Wetterdaten/KL_Tageswerte_Beschreibung_Stationen.txt"

if not Path(data_dir).exists():
    print(f"{data_dir} Ordner existiert nicht, bitte zuerst 2-extractor.py ausführen")
    exit()

if not Path(db_path).exists():
    print(f"{db_path} existiert nicht, bitte zuerst 3-create_db.py ausführen")
    exit()

if not Path(station_file_path).exists():
    station_file_name = Path(station_file_path).name
    print(f"{station_file_name} existiert nicht, bitte zuerst 1-downloader.py ausführen")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM tbl_messwerte")
if cursor.fetchone()[0] > 0:
    print("Daten existieren bereits in der Datenbank, um Daten erneut zu importieren, bitte Datenbank löschen")
    exit()
conn.close()

csv_files = list(Path(data_dir).glob("produkt_klima_tag_*.txt"))
if not csv_files:
    print(f"Keine CSV Dateien gefunden in {data_dir}, bitte zuerst 2-extractor.py ausführen")
    exit()

print("Stationen werden importiert...")

valid_states = [
    "Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg",
    "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen",
    "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt", "Schleswig-Holstein", "Thüringen"
]

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(station_file_path, "r", encoding="latin-1") as f:
    lines = f.readlines()
    for line in lines[2:]:
        try:
            parts = line.split()
            if len(parts) < 8:
                continue
            
            station_id = int(parts[0])
            
            elevation = float(parts[3]) if parts[3].isdigit() else None
            latitude = float(parts[4]) if parts[4].replace(".", "").replace("-", "").isdigit() else None
            longitude = float(parts[5]) if parts[5].replace(".", "").replace("-", "").isdigit() else None
            
            if len(parts) > 7:
                if "Frei" in parts:
                    try:
                        frei_index = parts.index("Frei")
                        bundesland_parts = parts[7:frei_index]
                        bundesland = " ".join(bundesland_parts)
                    except ValueError:
                        bundesland = parts[7]
                else:
                    bundesland = parts[7]
            else:
                bundesland = ""
            
            if bundesland not in valid_states:
                bundesland = ""
            
            if len(parts) > 7 and parts[6].endswith(")") and "(" in parts[6]:
                station_name = parts[6] + " " + parts[7]
            else:
                station_name = parts[6]
            
            if station_name:
                cursor.execute("""
                    INSERT INTO tbl_stationen (STATIONS_ID, Stationsname, Bundesland, Stationshoehe, geoBreite, geoLaenge)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (station_id, station_name, bundesland, elevation, latitude, longitude))
        except (ValueError, IndexError):
            continue

print("Stationen importiert!")

print(".csv Dateien werden importiert...")

for csv_file in csv_files:
    with open(csv_file, "r") as c:
        reader = csv.reader(c, delimiter=";", skipinitialspace=True)
        header = next(reader)
        
        if header[-1].lower() == "eor":
            header = header[:-1]
        
        columns = ",".join(header)
        placeholders = ",".join(["?"] * len(header))
        insert_sql = f"INSERT INTO tbl_messwerte ({columns}) VALUES ({placeholders})"
        
        rows = []
        for row in reader:
            row = [cell.strip() for cell in row]
            if row and row[-1].lower() == "eor":
                row = row[:-1]
            if row:
                rows.append(row)
        
        cursor.executemany(insert_sql, rows)

conn.commit()
conn.close()

print(".csv Dateien importiert!")