import sqlite3
from pathlib import Path

db_path = "wetter.db"
data_dir = "Extrahierte_Wetterdaten"

if not Path(data_dir).exists():
    print(f"{data_dir} Ordner existiert nicht, bitte zuerst 2-extractor.py ausführen")
    exit()

if Path(db_path).exists():
    print(f"{db_path} existiert bereits, um Datenbank erneut zu erstellen, bitte Datenbank löschen")
    exit()

print("Datenbank wird erstellt...")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE tbl_stationen (
        STATIONS_ID INTEGER PRIMARY KEY,
        Stationsname TEXT,
        Bundesland TEXT,
        Stationshoehe REAL,
        geoBreite REAL,
        geoLaenge REAL
    )
""")

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
        TGK REAL,
        FOREIGN KEY (STATIONS_ID) REFERENCES tbl_stationen(STATIONS_ID)
    );
""")

conn.commit()
conn.close()
print("Datenbank erstellt!")
