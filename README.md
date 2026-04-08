# Wetterprojekt

## Vorbereitung

1. **Python 3.10+** erforderlich
2. Dependencies installieren:
   ```bash
   pip install -r requirements.txt
3. Ungefähr 7GB freien Speicherplatz
   ```

## Installation

```bash
git clone https://github.com/sean-imus/wetterprojekt.git
cd wetterprojekt
```

## Nutzung

Führ die Skripte der Reihe nach aus:

```bash
python 1-downloader.py
python 2-extractor.py
python 3-create_db.py
python 4-import_to_db.py
python 5-fix_values.py
python 6-main.py
```

## Skripte

| Skript | Beschreibung |
|--------|---------------|
| 1-downloader.py | Lädt Wetterdaten vom DWD runter |
| 2-extractor.py | Entpackt die ZIP-Dateien |
| 3-create_db.py | Erstellt die SQLite-Datenbank und die Tabellen |
| 4-import_to_db.py | Importiert Stationsmetadaten und CSV-Daten in die Datenbank |
| 5-fix_values.py | Ersetzt -999 durch NULL und erstellt Indizes |
| 6-main.py | GUI zum Abfragen und Visualisieren der Daten |

## Funktionen

- Stationenauswahl nach Bundesland oder ganz Deutschland
- Stationen durch Eingabe filtern
- Mehrere Wettermetriken (Temperatur, Niederschlag, Schneehöhe, Wind, etc.)
- Benutzerdefinierter Zeitraum (TT.MM.JJJJ Format)
- Matplotlib-Visualisierung
- Statistiken: Durchschnitt, Minimum, Maximum

## Datenbankschema

- `tbl_stationen` - Stationsmetadaten (ID, Name, Bundesland, Höhe, Koordinaten)
- `tbl_messwerte` - Wetterdaten mit Fremdschlüssel zu tbl_stationen

## Datenquelle

Wetterdaten vom [Deutschen Wetterdienst (DWD)](https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/)
