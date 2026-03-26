import sqlite3
from pathlib import Path

db_file = "wetter.db"

if not Path(db_file).exists():
    print(f"{db_file} existiert nicht, bitte zuerst 4-csv_to_sql.py ausführen")
    exit()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM tbl_messwerte WHERE FX = -999 OR FM = -999 OR RSK = -999 OR RSKF = -999 OR SDK = -999 OR SHK_TAG = -999 OR NM = -999 OR VPM = -999 OR PM = -999 OR TMK = -999 OR TXK = -999 OR TNK = -999 OR TGK = -999 OR QN_3 = -999 OR QN_4 = -999 OR UPM = -999")
if cursor.fetchone()[0] == 0:
    print("Keine -999 Werte gefunden")
    exit()

conn.close()

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

count = 0

cursor.execute("UPDATE tbl_messwerte SET FX = NULL WHERE FX = -999")
count += cursor.rowcount
print("FX ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET FM = NULL WHERE FM = -999")
count += cursor.rowcount
print("FM ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET RSK = NULL WHERE RSK = -999")
count += cursor.rowcount
print("RSK ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET RSKF = NULL WHERE RSKF = -999")
count += cursor.rowcount
print("RSKF ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET SDK = NULL WHERE SDK = -999")
count += cursor.rowcount
print("SDK ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET SHK_TAG = NULL WHERE SHK_TAG = -999")
count += cursor.rowcount
print("SHK_TAG ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET NM = NULL WHERE NM = -999")
count += cursor.rowcount
print("NM ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET VPM = NULL WHERE VPM = -999")
count += cursor.rowcount
print("VPM ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET PM = NULL WHERE PM = -999")
count += cursor.rowcount
print("PM ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET TMK = NULL WHERE TMK = -999")
count += cursor.rowcount
print("TMK ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET TXK = NULL WHERE TXK = -999")
count += cursor.rowcount
print("TXK ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET TNK = NULL WHERE TNK = -999")
count += cursor.rowcount
print("TNK ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET TGK = NULL WHERE TGK = -999")
count += cursor.rowcount
print("TGK ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET QN_3 = NULL WHERE QN_3 = -999")
count += cursor.rowcount
print("QN_3 ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET QN_4 = NULL WHERE QN_4 = -999")
count += cursor.rowcount
print("QN_4 ersetzt!")

cursor.execute("UPDATE tbl_messwerte SET UPM = NULL WHERE UPM = -999")
count += cursor.rowcount
print("UPM ersetzt!")

conn.commit()
conn.close()

print(f"{count} Werte ersetzt!")
