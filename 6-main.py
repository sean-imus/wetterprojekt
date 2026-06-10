import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from weather_db import WeatherDB

db_path = "wetter.db"

if not Path(db_path).exists():
    print("Datenbank nicht gefunden!")
    exit()

db = WeatherDB(db_path)
states = db.states
stations_data = db.stations_data
min_year = db.min_year
max_year = db.max_year

col_map = {
    "Temperatur (Mittel)": "TMK",
    "Temperatur (Max)": "TXK",
    "Temperatur (Min)": "TNK",
    "Niederschlag": "RSK",
    "Schneehöhe": "SHK_TAG",
    "Wind (Max)": "FX",
    "Wind (Mittel)": "FM",
    "Sonnenscheindauer": "SDK",
    "Luftdruck": "PM",
    "Luftfeuchtigkeit": "UPM",
    "Bedeckung": "NM",
}

unit_map = {
    "Temperatur (Mittel)": "°C",
    "Temperatur (Max)": "°C",
    "Temperatur (Min)": "°C",
    "Niederschlag": "mm",
    "Schneehöhe": "cm",
    "Wind (Max)": "km/h",
    "Wind (Mittel)": "km/h",
    "Sonnenscheindauer": "h",
    "Luftdruck": "hPa",
    "Luftfeuchtigkeit": "%",
    "Bedeckung": "%",
}

metrics = list(col_map.keys())


def stationen_laden(bundesland):
    stationen = []
    for sid, data in stations_data.items():
        if bundesland == "Alle" or data["state"] == bundesland:
            stationen.append((sid, data["name"]))
    stationen.sort(key=lambda x: x[1])
    return stationen


root = tk.Tk()
root.title("Wetterdaten")
root.geometry("920x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=5, pady=5)


# Tab 1: Tagesdaten

tab_daily = ttk.Frame(notebook)
notebook.add(tab_daily, text="Tagesdaten")

selected_station = tk.StringVar()
selected_state = tk.StringVar(value="Alle")
selected_metric = tk.StringVar(value="Temperatur (Mittel)")

top = ttk.Frame(tab_daily, padding="10")
top.pack(fill="x")

ttk.Label(top, text="Bundesland:").pack(side="left", padx=5)
state_combo = ttk.Combobox(
    top, textvariable=selected_state, values=states, state="normal", width=18
)
state_combo.pack(side="left", padx=5)

ttk.Label(top, text="Station:").pack(side="left", padx=5)
station_combo = ttk.Combobox(
    top, textvariable=selected_station, state="normal", width=25
)
station_combo.pack(side="left", padx=5)

ttk.Label(top, text="Metrik:").pack(side="left", padx=5)
ttk.Combobox(
    top, textvariable=selected_metric, values=metrics, state="readonly", width=18
).pack(side="left", padx=5)

middle = ttk.Frame(tab_daily, padding="10")
middle.pack(fill="x")

ttk.Label(middle, text="Start:").pack(side="left", padx=5)
start_day = ttk.Spinbox(middle, from_=1, to=31, width=4)
start_day.set(1)
start_day.pack(side="left", padx=2)
start_month = ttk.Spinbox(middle, from_=1, to=12, width=4)
start_month.set(1)
start_month.pack(side="left", padx=2)
start_year = ttk.Spinbox(middle, from_=min_year, to=max_year, width=6)
start_year.set(min_year)
start_year.pack(side="left", padx=2)

ttk.Label(middle, text="Bis:").pack(side="left", padx=10)
end_day = ttk.Spinbox(middle, from_=1, to=31, width=4)
end_day.set(31)
end_day.pack(side="left", padx=2)
end_month = ttk.Spinbox(middle, from_=1, to=12, width=4)
end_month.set(12)
end_month.pack(side="left", padx=2)
end_year = ttk.Spinbox(middle, from_=min_year, to=max_year, width=6)
end_year.set(max_year)
end_year.pack(side="left", padx=2)

ttk.Button(middle, text="Abfrage starten", command=lambda: run_daily_query()).pack(
    side="left", padx=15
)

chart_frame = ttk.Frame(tab_daily, padding="10")
chart_frame.pack(fill="both", expand=True)
fig = Figure(figsize=(8, 4))
ax = fig.add_subplot(111)
canvas = FigureCanvasTkAgg(fig, master=chart_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)

stats_frame = ttk.LabelFrame(tab_daily, text="Auswertung", padding="10")
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


def bundesland_geaendert(event=None):
    stationen = stationen_laden(selected_state.get())
    station_combo["values"] = [f"{name} ({sid})" for sid, name in stationen]
    selected_station.set("")


def station_suchen(event=None):
    eingabe = selected_station.get().lower()
    stationen = stationen_laden(selected_state.get())
    ergebnisse = []
    for sid, name in stationen:
        if name.lower().startswith(eingabe):
            ergebnisse.append(f"{name} ({sid})")
    station_combo["values"] = ergebnisse


def run_daily_query():
    station_str = selected_station.get()
    if not station_str:
        messagebox.showwarning("Fehler", "Bitte eine Station auswählen")
        return

    station_id = station_str.split("(")[1].split(")")[0]
    metric = selected_metric.get()
    col = col_map[metric]
    unit = unit_map[metric]

    start_date = (
        f"{start_year.get()}{int(start_month.get()):02d}{int(start_day.get()):02d}"
    )
    end_date = f"{end_year.get()}{int(end_month.get()):02d}{int(end_day.get()):02d}"

    if start_date > end_date:
        messagebox.showwarning("Fehler", "Startdatum muss vor Enddatum liegen")
        return

    ergebnisse = db.get_measurements(station_id, col, start_date, end_date)
    if not ergebnisse:
        messagebox.showinfo(
            "Keine Daten", "Keine Daten für diese Station im gewählten Zeitraum"
        )
        return

    datumsangaben = [r[0] for r in ergebnisse]
    werte = [r[1] for r in ergebnisse]
    if metric == "Bedeckung":
        werte = [v * 12.5 for v in werte]

    anzeige_daten = [f"{d[6:8]}.{d[4:6]}.{d[0:4]}" for d in datumsangaben]

    ax.clear()
    ax.plot(anzeige_daten, werte, marker="o", markersize=4, linewidth=1.5)
    ax.set_title(f"{metric} – Station {station_id}")
    ax.set_xlabel("Datum")
    ax.set_ylabel(f"{metric} ({unit})")
    ax.grid(True, alpha=0.3)
    schritt = max(1, len(anzeige_daten) // 8)
    ax.set_xticks(range(0, len(anzeige_daten), schritt))
    ax.set_xticklabels(
        [anzeige_daten[i] for i in range(0, len(anzeige_daten), schritt)],
        rotation=45,
        ha="right",
    )
    fig.tight_layout()
    canvas.draw()

    durchschnitt = sum(werte) / len(werte)
    avg_label.config(text=f"Durchschnitt: {durchschnitt:.1f} {unit}")
    min_label.config(text=f"Minimum: {min(werte):.1f} {unit}")
    max_label.config(text=f"Maximum: {max(werte):.1f} {unit}")


state_combo.bind("<<ComboboxSelected>>", bundesland_geaendert)
station_combo.bind("<KeyRelease>", station_suchen)

stationen = stationen_laden("Alle")
station_combo["values"] = [f"{name} ({sid})" for sid, name in stationen]


# Tab 2: Aggregation

tab_agg = ttk.Frame(notebook)
notebook.add(tab_agg, text="Aggregation")

agg_mode = tk.StringVar(value="Jahreswerte")
agg_metric = tk.StringVar(value="Temperatur (Mittel)")
agg_all_stations = tk.BooleanVar(value=True)
agg_state = tk.StringVar(value="Alle")
agg_station = tk.StringVar()

agg_row1 = ttk.Frame(tab_agg, padding="10")
agg_row1.pack(fill="x")

ttk.Radiobutton(
    agg_row1,
    text="Jahreswerte",
    variable=agg_mode,
    value="Jahreswerte",
    command=lambda: modus_wechseln(),
).pack(side="left", padx=5)
ttk.Radiobutton(
    agg_row1,
    text="Monatswerte",
    variable=agg_mode,
    value="Monatswerte",
    command=lambda: modus_wechseln(),
).pack(side="left", padx=5)
ttk.Label(agg_row1, text="Metrik:").pack(side="left", padx=(20, 5))
ttk.Combobox(
    agg_row1, textvariable=agg_metric, values=metrics, state="readonly", width=18
).pack(side="left", padx=5)

agg_row2 = ttk.Frame(tab_agg, padding=(10, 0))
agg_row2.pack(fill="x")

agg_range_sub = ttk.Frame(agg_row2)
agg_range_sub.pack(side="left")
ttk.Label(agg_range_sub, text="Von Jahr:").pack(side="left", padx=5)
agg_from_year = ttk.Spinbox(agg_range_sub, from_=min_year, to=max_year, width=6)
agg_from_year.set(max(min_year, max_year - 20))
agg_from_year.pack(side="left", padx=2)
ttk.Label(agg_range_sub, text="Bis Jahr:").pack(side="left", padx=(10, 5))
agg_to_year = ttk.Spinbox(agg_range_sub, from_=min_year, to=max_year, width=6)
agg_to_year.set(max_year)
agg_to_year.pack(side="left", padx=2)

agg_single_sub = ttk.Frame(agg_row2)
ttk.Label(agg_single_sub, text="Jahr:").pack(side="left", padx=5)
agg_single_year = ttk.Spinbox(agg_single_sub, from_=min_year, to=max_year, width=6)
agg_single_year.set(max_year)
agg_single_year.pack(side="left", padx=2)

agg_row3 = ttk.Frame(tab_agg, padding=(10, 0))
agg_row3.pack(fill="x")

ttk.Checkbutton(
    agg_row3,
    text="Alle Stationen",
    variable=agg_all_stations,
    command=lambda: stationsfilter_wechseln(),
).pack(side="left", padx=5)

agg_station_filter = ttk.Frame(agg_row3)
ttk.Label(agg_station_filter, text="Bundesland:").pack(side="left", padx=5)
agg_state_combo = ttk.Combobox(
    agg_station_filter, textvariable=agg_state, values=states, state="normal", width=18
)
agg_state_combo.pack(side="left", padx=5)
ttk.Label(agg_station_filter, text="Station:").pack(side="left", padx=5)
agg_station_combo = ttk.Combobox(
    agg_station_filter, textvariable=agg_station, state="normal", width=25
)
agg_station_combo.pack(side="left", padx=5)

agg_row4 = ttk.Frame(tab_agg, padding=(10, 5))
agg_row4.pack(fill="x")
ttk.Button(agg_row4, text="Abfrage starten", command=lambda: run_agg_query()).pack(
    side="left"
)

agg_chart_frame = ttk.Frame(tab_agg, padding="10")
agg_chart_frame.pack(fill="both", expand=True)
agg_fig = Figure(figsize=(8, 4))
agg_ax = agg_fig.add_subplot(111)
agg_canvas = FigureCanvasTkAgg(agg_fig, master=agg_chart_frame)
agg_canvas.get_tk_widget().pack(fill="both", expand=True)

agg_stats = ttk.LabelFrame(tab_agg, text="Auswertung", padding="10")
agg_stats.pack(fill="x", padx=10, pady=5)
agg_stats.columnconfigure(0, weight=1)
agg_stats.columnconfigure(1, weight=1)
agg_stats.columnconfigure(2, weight=1)
agg_avg_label = ttk.Label(agg_stats, text="Durchschnitt: -", font=("Arial", 12, "bold"))
agg_avg_label.grid(row=0, column=0, padx=10)
agg_min_label = ttk.Label(agg_stats, text="Minimum: -", font=("Arial", 12, "bold"))
agg_min_label.grid(row=0, column=1, padx=10)
agg_max_label = ttk.Label(agg_stats, text="Maximum: -", font=("Arial", 12, "bold"))
agg_max_label.grid(row=0, column=2, padx=10)


def modus_wechseln():
    if agg_mode.get() == "Jahreswerte":
        agg_single_sub.pack_forget()
        agg_range_sub.pack(side="left")
    else:
        agg_range_sub.pack_forget()
        agg_single_sub.pack(side="left")


def stationsfilter_wechseln():
    if agg_all_stations.get():
        agg_station_filter.pack_forget()
    else:
        agg_station_filter.pack(side="left")


def agg_bundesland_geaendert(event=None):
    stationen = stationen_laden(agg_state.get())
    agg_station_combo["values"] = [f"{name} ({sid})" for sid, name in stationen]
    agg_station.set("")


def agg_station_suchen(event=None):
    eingabe = agg_station.get().lower()
    stationen = stationen_laden(agg_state.get())
    ergebnisse = []
    for sid, name in stationen:
        if name.lower().startswith(eingabe):
            ergebnisse.append(f"{name} ({sid})")
    agg_station_combo["values"] = ergebnisse


def run_agg_query():
    metric = agg_metric.get()
    col = col_map[metric]
    unit = unit_map[metric]
    modus = agg_mode.get()

    station_id = None
    if not agg_all_stations.get():
        station_str = agg_station.get()
        if not station_str:
            messagebox.showwarning(
                "Fehler",
                "Bitte eine Station auswählen oder 'Alle Stationen' aktivieren",
            )
            return
        station_id = station_str.split("(")[1].split(")")[0]

    if modus == "Jahreswerte":
        von_jahr = int(agg_from_year.get())
        bis_jahr = int(agg_to_year.get())
        if von_jahr > bis_jahr:
            messagebox.showwarning("Fehler", "Von-Jahr muss vor Bis-Jahr liegen")
            return
        ergebnisse = db.get_yearly_averages(col, von_jahr, bis_jahr, station_id)
        beschriftungen = [r[0] for r in ergebnisse]
        x_titel = "Jahr"
    else:
        jahr = int(agg_single_year.get())
        ergebnisse = db.get_monthly_averages(col, jahr, station_id)
        monatsnamen = [
            "Jan",
            "Feb",
            "Mär",
            "Apr",
            "Mai",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Okt",
            "Nov",
            "Dez",
        ]
        beschriftungen = [monatsnamen[int(r[0]) - 1] for r in ergebnisse]
        x_titel = "Monat"

    if not ergebnisse:
        messagebox.showinfo("Keine Daten", "Keine Daten für diesen Zeitraum gefunden")
        return

    werte = [r[1] for r in ergebnisse]
    station_label = "Alle Stationen" if not station_id else f"Station {station_id}"

    agg_ax.clear()
    agg_ax.bar(range(len(beschriftungen)), werte, color="steelblue", edgecolor="white")
    agg_ax.set_xticks(range(len(beschriftungen)))
    agg_ax.set_xticklabels(beschriftungen, rotation=45, ha="right")
    agg_ax.set_title(f"{metric} – {station_label}")
    agg_ax.set_xlabel(x_titel)
    agg_ax.set_ylabel(f"Durchschnitt {metric} ({unit})")
    agg_ax.grid(True, alpha=0.3, axis="y")
    agg_fig.tight_layout()
    agg_canvas.draw()

    durchschnitt = sum(werte) / len(werte)
    agg_avg_label.config(text=f"Durchschnitt: {durchschnitt:.1f} {unit}")
    agg_min_label.config(text=f"Minimum: {min(werte):.1f} {unit}")
    agg_max_label.config(text=f"Maximum: {max(werte):.1f} {unit}")


agg_state_combo.bind("<<ComboboxSelected>>", agg_bundesland_geaendert)
agg_station_combo.bind("<KeyRelease>", agg_station_suchen)

agg_station_filter.pack_forget()
agg_station_combo["values"] = [
    f"{name} ({sid})" for sid, name in stationen_laden("Alle")
]


root.mainloop()
