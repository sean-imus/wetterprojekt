import sqlite3
from pathlib import Path

db_file = "wetter.db"
data_folder = "Extrahierte_Wetterdaten"

if not Path(data_folder).exists():
    print(f"{data_folder} Ordner existiert nicht, bitte zuerst 2-extractor.py ausführen")
    exit()

if Path(db_file).exists():
    print(f"{db_file} existiert bereits, um Datenbank erneut zu erstellen, bitte Datenbank löschen")
    exit()

print("Datenbank wird erstellt...")

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE tbl_messwerte (
        Mid INTEGER PRIMARY KEY AUTOINCREMENT,
        STATIONS_ID INTEGER,
        MESS_DATUM TEXT,
        QN_3 INTEGER,
        FX REAL,
        FM REAL,
        QN_4 INTEGER,
        RSK REAL,
        RSKF REAL,
        SDK REAL,
        SHK_TAG REAL,
        NM REAL,
        VPM REAL,
        PM REAL,
        TMK REAL,
        UPM INTEGER,
        TXK REAL,
        TNK REAL,
        TGK REAL
    );
""")

conn.commit()
conn.close()
print("Datenbank erstellt!")
