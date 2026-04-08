import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path

db_path = "wetter.db"

if not Path(db_path).exists():
    print("Datenbank nicht gefunden!")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM tbl_stationen")
if cursor.fetchone()[0] == 0:
    print("Stationstabelle existiert nicht, bitte zuerst 4-csv_to_sql.py ausführen")
    exit()

cursor.execute("SELECT DISTINCT Bundesland FROM tbl_stationen WHERE Bundesland != '' ORDER BY Bundesland")
states = ["Alle"] + [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT STATIONS_ID, Stationsname, Bundesland FROM tbl_stationen ORDER BY Stationsname")
stations_data = {}
for row in cursor.fetchall():
    stations_data[row[0]] = {"name": row[1], "state": row[2]}

cursor.execute("SELECT MIN(MESS_DATUM), MAX(MESS_DATUM) FROM tbl_messwerte")
date_range = cursor.fetchone()
min_year = int(date_range[0][:4]) if date_range[0] else 1900
max_year = int(date_range[1][:4]) if date_range[1] else 2100

conn.close()

root = tk.Tk()
root.title("Wetterdaten")
root.geometry("850x650")

selected_station = tk.StringVar()
selected_state = tk.StringVar(value="Alle")
selected_metric = tk.StringVar(value="Temperatur (Mittel)")

top = ttk.Frame(root, padding="10")
top.pack(fill="x")

ttk.Label(top, text="Bundesland:").pack(side="left", padx=5)
state_combo = ttk.Combobox(top, textvariable=selected_state, values=states, state="normal", width=18)
state_combo.pack(side="left", padx=5)

ttk.Label(top, text="Station:").pack(side="left", padx=5)
station_combo = ttk.Combobox(top, textvariable=selected_station, state="normal", width=25)
station_combo.pack(side="left", padx=5)

ttk.Label(top, text="Metrik:").pack(side="left", padx=5)
metric_combo = ttk.Combobox(top, textvariable=selected_metric, values=[
    "Temperatur (Mittel)", "Temperatur (Max)", "Temperatur (Min)",
    "Niederschlag", "Schneehöhe", "Wind (Max)", "Wind (Mittel)",
    "Sonnenscheindauer", "Luftdruck", "Luftfeuchtigkeit", "Bedeckung"
], state="readonly", width=18)
metric_combo.pack(side="left", padx=5)

middle = ttk.Frame(root, padding="10")
middle.pack(fill="x")

ttk.Label(middle, text="Start:").pack(side="left", padx=5)
start_day = ttk.Spinbox(middle, from_=1, to=31, width=4)
start_day.pack(side="left", padx=2)
start_day.set(1)
start_month = ttk.Spinbox(middle, from_=1, to=12, width=4)
start_month.pack(side="left", padx=2)
start_month.set(1)
start_year = ttk.Spinbox(middle, from_=min_year, to=max_year, width=6)
start_year.pack(side="left", padx=2)
start_year.set(min_year)

ttk.Label(middle, text="Bis:").pack(side="left", padx=10)
end_day = ttk.Spinbox(middle, from_=1, to=31, width=4)
end_day.pack(side="left", padx=2)
end_day.set(31)
end_month = ttk.Spinbox(middle, from_=1, to=12, width=4)
end_month.pack(side="left", padx=2)
end_month.set(12)
end_year = ttk.Spinbox(middle, from_=min_year, to=max_year, width=6)
end_year.pack(side="left", padx=2)
end_year.set(max_year)

chart_frame = ttk.Frame(root, padding="10")
chart_frame.pack(fill="both", expand=True)

fig = Figure(figsize=(8, 4))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

stats_frame = ttk.LabelFrame(root, text="Auswertung", padding="10")
stats_frame.pack(fill="x", padx=10, pady=5)

stats_frame.columnconfigure(0, weight=1)
stats_frame.columnconfigure(1, weight=1)
stats_frame.columnconfigure(2, weight=1)

avg_label = ttk.Label(stats_frame, text="Durchschnitt: -", font=("Arial", 12, "bold"))
avg_label.grid(row=0, column=0, padx=10)

min_label = ttk.Label(stats_frame, text="Minimum: -", font=("Arial", 12, "bold"))
min_label.grid(row=0, column=1, padx=10)

max_label = ttk.Label(stats_frame, text="Maximum: -", font=("Arial", 12, "bold"))
max_label.grid(row=0, column=2, padx=10)

col_map = {
    "Temperatur (Mittel)": "TMK", "Temperatur (Max)": "TXK", "Temperatur (Min)": "TNK",
    "Niederschlag": "RSK", "Schneehöhe": "SHK_TAG", "Wind (Max)": "FX",
    "Wind (Mittel)": "FM", "Sonnenscheindauer": "SDK", "Luftdruck": "PM",
    "Luftfeuchtigkeit": "UPM", "Bedeckung": "NM"
}

unit_map = {
    "Temperatur (Mittel)": "°C", "Temperatur (Max)": "°C", "Temperatur (Min)": "°C",
    "Niederschlag": "mm", "Schneehöhe": "cm", "Wind (Max)": "km/h",
    "Wind (Mittel)": "km/h", "Sonnenscheindauer": "h", "Luftdruck": "hPa",
    "Luftfeuchtigkeit": "%", "Bedeckung": "%"
}


def get_max_day(month, year):
    if month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 29
        return 28
    return 31


def validate_spinbox(day_spinbox, month_spinbox, year_spinbox):
    try:
        month = int(month_spinbox.get())
        year = int(year_spinbox.get())
        if 1 <= month <= 12 and min_year <= year <= max_year:
            max_day = get_max_day(month, year)
            day_spinbox.config(to=max_day)
            current_val = int(day_spinbox.get())
            if current_val > max_day:
                day_spinbox.set(max_day)
    except ValueError:
        pass


def get_filtered_stations(state=None):
    if state == "Alle" or not state:
        stations = [(sid, data["name"]) for sid, data in stations_data.items()]
    else:
        stations = [(sid, data["name"]) for sid, data in stations_data.items() if data["state"] == state]
    return sorted(stations, key=lambda x: x[1])


def filter_station(*args):
    typed = selected_station.get().lower()
    state = selected_state.get()
    stations = get_filtered_stations(state)

    if typed == "":
        station_options = stations
    else:
        station_options = [(sid, name) for sid, name in stations if name.lower().startswith(typed)]

    station_combo["values"] = [f"{name} ({sid})" for sid, name in station_options]


def on_state_changed(*args):
    state = selected_state.get()
    stations = get_filtered_stations(state)
    station_combo["values"] = [f"{name} ({sid})" for sid, name in stations]
    selected_station.set("")


def parse_date(day_spinbox, month_spinbox, year_spinbox):
    try:
        day = int(day_spinbox.get())
        month = int(month_spinbox.get())
        year = int(year_spinbox.get())
        max_day = get_max_day(month, year)
        if not (1 <= day <= max_day and 1 <= month <= 12 and min_year <= year <= max_year):
            return None
        return f"{year}{month:02d}{day:02d}"
    except ValueError:
        return None


def run_query():
    station_str = selected_station.get()
    if not station_str:
        messagebox.showwarning("Fehler", "Bitte eine Station auswählen")
        return

    station_id = station_str.split("(")[1].split(")")[0]
    metric = selected_metric.get()

    col = col_map.get(metric)
    unit = unit_map.get(metric)

    start_date = parse_date(start_day, start_month, start_year)
    end_date = parse_date(end_day, end_month, end_year)

    if not start_date or not end_date:
        messagebox.showwarning("Fehler", "Ungültiges Datum")
        return

    if start_date > end_date:
        messagebox.showwarning("Fehler", "Startdatum muss vor Enddatum liegen")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        if start_date == end_date:
            cursor.execute(f"""
                SELECT MESS_DATUM, {col} 
                FROM tbl_messwerte 
                WHERE STATIONS_ID = ? AND {col} IS NOT NULL AND MESS_DATUM = ?
                ORDER BY MESS_DATUM
            """, (station_id, start_date))
        else:
            cursor.execute(f"""
                SELECT MESS_DATUM, {col} 
                FROM tbl_messwerte 
                WHERE STATIONS_ID = ? AND {col} IS NOT NULL AND MESS_DATUM >= ? AND MESS_DATUM <= ?
                ORDER BY MESS_DATUM
            """, (station_id, start_date, end_date))

        results = cursor.fetchall()
    finally:
        conn.close()

    if not results:
        messagebox.showinfo("Keine Daten", "Keine Daten für diese Station im gewählten Zeitraum")
        return

    dates = [r[0] for r in results]
    values = [r[1] for r in results]

    avg = sum(values) / len(values)
    min_val = min(values)
    max_val = max(values)

    display_dates = [f"{d[6:8]}.{d[4:6]}.{d[0:4]}" if len(d) == 8 else d for d in dates]

    ax.clear()
    ax.plot(display_dates, values, marker="o", markersize=4, linewidth=1.5)
    ax.set_title(f"{metric} - Station {station_id}")
    ax.set_xlabel("Datum")
    ax.set_ylabel(f"{metric} ({unit})")
    ax.grid(True, alpha=0.3)

    step = max(1, len(display_dates) // 8)
    ax.set_xticks(range(0, len(display_dates), step))
    ax.set_xticklabels([display_dates[i] for i in range(0, len(display_dates), step)], rotation=45, ha="right")

    fig.tight_layout()
    canvas.draw()

    avg_label.config(text=f"Durchschnitt: {avg:.1f} {unit}")
    min_label.config(text=f"Minimum: {min_val:.1f} {unit}")
    max_label.config(text=f"Maximum: {max_val:.1f} {unit}")


state_combo.bind("<<ComboboxSelected>>", on_state_changed)
station_combo.bind("<KeyRelease>", filter_station)

for spinbox in (start_day, start_month, start_year):
    spinbox.bind("<<Increment>>", lambda e: validate_spinbox(start_day, start_month, start_year))
    spinbox.bind("<<Decrement>>", lambda e: validate_spinbox(start_day, start_month, start_year))

for spinbox in (end_day, end_month, end_year):
    spinbox.bind("<<Increment>>", lambda e: validate_spinbox(end_day, end_month, end_year))
    spinbox.bind("<<Decrement>>", lambda e: validate_spinbox(end_day, end_month, end_year))

validate_spinbox(end_day, end_month, end_year)

ttk.Button(middle, text="Abfrage starten", command=run_query).pack(side="left", padx=15)

stations = get_filtered_stations("Alle")
station_combo["values"] = [f"{name} ({sid})" for sid, name in stations]

root.mainloop()
