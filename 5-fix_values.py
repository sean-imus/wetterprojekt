import sqlite3
from pathlib import Path

db_path = "wetter.db"

if not Path(db_path).exists():
    print(f"{db_path} existiert nicht, bitte zuerst 4-import_to_db.py ausführen")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("""
    SELECT COUNT(*) FROM tbl_messwerte 
    WHERE FX = -999 OR FM = -999 OR RSK = -999 OR RSKF = -999 OR SDK = -999 
    OR SHK_TAG = -999 OR NM = -999 OR VPM = -999 OR PM = -999 OR TMK = -999 
    OR TXK = -999 OR TNK = -999 OR TGK = -999 OR QN_3 = -999 OR QN_4 = -999 
    OR UPM = -999
""")

if cursor.fetchone()[0] == 0:
    print("Keine -999 Werte gefunden")
    exit()

print("Werte werden ersetzt...")

cursor.execute("""
    UPDATE tbl_messwerte SET
        FX = CASE WHEN FX = -999 THEN NULL ELSE FX END,
        FM = CASE WHEN FM = -999 THEN NULL ELSE FM END,
        RSK = CASE WHEN RSK = -999 THEN NULL ELSE RSK END,
        RSKF = CASE WHEN RSKF = -999 THEN NULL ELSE RSKF END,
        SDK = CASE WHEN SDK = -999 THEN NULL ELSE SDK END,
        SHK_TAG = CASE WHEN SHK_TAG = -999 THEN NULL ELSE SHK_TAG END,
        NM = CASE WHEN NM = -999 THEN NULL ELSE NM END,
        VPM = CASE WHEN VPM = -999 THEN NULL ELSE VPM END,
        PM = CASE WHEN PM = -999 THEN NULL ELSE PM END,
        TMK = CASE WHEN TMK = -999 THEN NULL ELSE TMK END,
        TXK = CASE WHEN TXK = -999 THEN NULL ELSE TXK END,
        TNK = CASE WHEN TNK = -999 THEN NULL ELSE TNK END,
        TGK = CASE WHEN TGK = -999 THEN NULL ELSE TGK END,
        QN_3 = CASE WHEN QN_3 = -999 THEN NULL ELSE QN_3 END,
        QN_4 = CASE WHEN QN_4 = -999 THEN NULL ELSE QN_4 END,
        UPM = CASE WHEN UPM = -999 THEN NULL ELSE UPM END
    WHERE FX = -999 OR FM = -999 OR RSK = -999 OR RSKF = -999 OR SDK = -999 
    OR SHK_TAG = -999 OR NM = -999 OR VPM = -999 OR PM = -999 OR TMK = -999 
    OR TXK = -999 OR TNK = -999 OR TGK = -999 OR QN_3 = -999 OR QN_4 = -999 
    OR UPM = -999
""")

conn.commit()

print("Werte ersetzt!")

print("Erstellung der Indexe...")
cursor.execute("CREATE INDEX idx_stations_id ON tbl_messwerte(STATIONS_ID);")
cursor.execute("CREATE INDEX idx_mess_datum ON tbl_messwerte(MESS_DATUM);")
cursor.execute("CREATE INDEX idx_stationen_id ON tbl_stationen(STATIONS_ID);")
cursor.execute("CREATE INDEX idx_messwerte_station_date ON tbl_messwerte(STATIONS_ID, MESS_DATUM);")
cursor.execute("CREATE INDEX idx_stationen_bundesland ON tbl_stationen(Bundesland);")
cursor.execute("CREATE INDEX idx_stationen_name ON tbl_stationen(Stationsname);")
print("Indexe erstellt!")

conn.close()
