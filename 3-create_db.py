import sqlite3
from pathlib import Path

output_file = "wetter.db"

def create_database():
    db_path = Path(output_file)
    if db_path.exists():
        print(f"{output_file} Datei existiert bereits, um Datenbank erneut zu erstellen, bitte Datenbank löschen")
        exit()

    conn = sqlite3.connect(output_file)
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
    print(f"{output_file} Datei erstellt!")

create_database()
