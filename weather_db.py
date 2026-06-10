import sqlite3


class WeatherDB:
    def __init__(self, db_path):
        self.db_path = db_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT DISTINCT Bundesland FROM tbl_stationen WHERE Bundesland != '' ORDER BY Bundesland"
        )
        self.states = ["Alle"] + [row[0] for row in cursor.fetchall()]

        cursor.execute(
            "SELECT STATIONS_ID, Stationsname, Bundesland FROM tbl_stationen ORDER BY Stationsname"
        )
        self.stations_data = {}
        for row in cursor.fetchall():
            self.stations_data[row[0]] = {"name": row[1], "state": row[2]}

        cursor.execute("SELECT MIN(MESS_DATUM), MAX(MESS_DATUM) FROM tbl_messwerte")
        date_range = cursor.fetchone()
        self.min_year = int(date_range[0][:4]) if date_range[0] else 1900
        self.max_year = int(date_range[1][:4]) if date_range[1] else 2100

        conn.close()

    def get_measurements(self, station_id, col, start_date, end_date):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            if start_date == end_date:
                cursor.execute(
                    f"""
                    SELECT MESS_DATUM, {col}
                    FROM tbl_messwerte
                    WHERE STATIONS_ID = ? AND {col} IS NOT NULL AND MESS_DATUM = ?
                    ORDER BY MESS_DATUM
                """,
                    (station_id, start_date),
                )
            else:
                cursor.execute(
                    f"""
                    SELECT MESS_DATUM, {col}
                    FROM tbl_messwerte
                    WHERE STATIONS_ID = ? AND {col} IS NOT NULL AND MESS_DATUM >= ? AND MESS_DATUM <= ?
                    ORDER BY MESS_DATUM
                """,
                    (station_id, start_date, end_date),
                )
            return cursor.fetchall()
        finally:
            conn.close()
