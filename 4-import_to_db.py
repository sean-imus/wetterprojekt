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
    print("Stationsdatei nicht gefunden, bitte zuerst 1-downloader.py ausführen")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM tbl_messwerte")
if cursor.fetchone()[0] > 0:
    print(
        "Daten existieren bereits in der Datenbank, um Daten erneut zu importieren, bitte Datenbank löschen"
    )
    exit()

csv_files = list(Path(data_dir).glob("produkt_klima_tag_*.txt"))
if not csv_files:
    print(
        f"Keine CSV Dateien gefunden in {data_dir}, bitte zuerst 2-extractor.py ausführen"
    )
    exit()

valid_states = [
    "Baden-Württemberg",
    "Bayern",
    "Berlin",
    "Brandenburg",
    "Bremen",
    "Hamburg",
    "Hessen",
    "Mecklenburg-Vorpommern",
    "Niedersachsen",
    "Nordrhein-Westfalen",
    "Rheinland-Pfalz",
    "Saarland",
    "Sachsen",
    "Sachsen-Anhalt",
    "Schleswig-Holstein",
    "Thüringen",
]

print("Stationen werden importiert...")

with open(station_file_path, "r", encoding="latin-1") as f:
    lines = f.readlines()

for line in lines[2:]:
    parts = line.split()
    if len(parts) < 7:
        continue

    try:
        station_id = int(parts[0])
        elevation = float(parts[3])
        latitude = float(parts[4])
        longitude = float(parts[5])
        station_name = parts[6]
        bundesland = parts[7] if len(parts) > 7 else ""

        if bundesland not in valid_states:
            bundesland = ""

        cursor.execute(
            "INSERT INTO tbl_stationen (STATIONS_ID, Stationsname, Bundesland, Stationshoehe, geoBreite, geoLaenge) VALUES (?, ?, ?, ?, ?, ?)",
            (station_id, station_name, bundesland, elevation, latitude, longitude),
        )
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
