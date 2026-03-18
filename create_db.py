import sqlite3
from pathlib import Path

DB_NAME = "wetter.db"

def create_database():
    db_path = Path(DB_NAME)
    if db_path.exists():
        db_path.unlink()
    
    conn = sqlite3.connect(DB_NAME)
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
    print("Done!")

create_database()
