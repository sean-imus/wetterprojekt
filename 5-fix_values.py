import sqlite3
from pathlib import Path

db_path = "wetter.db"

if not Path(db_path).exists():
    print(f"{db_path} existiert nicht, bitte zuerst 4-import_to_db.py ausführen")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Werte werden ersetzt...")

cursor.execute(
    """
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
"""
)

conn.commit()
print("Werte ersetzt!")

print("Indizes werden erstellt...")
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_stations_id ON tbl_messwerte(STATIONS_ID)"
)
cursor.execute("CREATE INDEX IF NOT EXISTS idx_mess_datum ON tbl_messwerte(MESS_DATUM)")
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_stationen_id ON tbl_stationen(STATIONS_ID)"
)
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_messwerte_station_date ON tbl_messwerte(STATIONS_ID, MESS_DATUM)"
)
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_stationen_bundesland ON tbl_stationen(Bundesland)"
)
cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_stationen_name ON tbl_stationen(Stationsname)"
)
conn.close()
print("Indizes erstellt!")
