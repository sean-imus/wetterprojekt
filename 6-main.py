import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

db_file = "wetter.db"

if not Path(db_file).exists():
    print(f"{db_file} existiert nicht, bitte zuerst 3-create_db.py ausführen")
    exit()
